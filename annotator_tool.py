import os
from datetime import datetime

import boto3
import streamlit as st
from streamlit.ScriptRunner import RerunException
from streamlit.ScriptRequestQueue import RerunData
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import exc
from PIL import Image

import database as db

load_dotenv(find_dotenv())

sqs_client = boto3.client('sqs', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                          region_name=os.getenv('AWS_REGION'))
sqs_queue_url = os.getenv('AWS_SQS_ANNOTATOR_QUEUE')


def main(session):
    st.sidebar.markdown('---')
    st.sidebar.title('Annotation tool')
    filename, pet_type = None, None
    using_sqs_queue = True
    if st.sidebar.checkbox('Set image filename:'):
        filename = st.sidebar.text_input('Filename:')
        if filename is not None:
            using_sqs_queue = False
    else:
        if session.message_value is None:
            session.message_value = get_next_sqs_message()
        if session.message_value is None:
            st.info('Queue is currently empty or messages are invisible')
        else:
            message_dict = eval(session.message_value['Body'])
            filename = message_dict['filename']
    st.sidebar.markdown(f'**filename:** {filename}')

    if filename is not None:
        st.markdown('## Image:')
        image = Image.open(os.path.join('PetImages', filename))
        st.image(image)

        bt_cat = st.sidebar.button('Cat')
        bt_dog = st.sidebar.button('Dog')
        bt_discard = st.sidebar.button('Discard image')

        if bt_cat:
            process_annotation(using_sqs_queue, filename, 'cat', session)
        elif bt_dog:
            process_annotation(using_sqs_queue, filename, 'dog', session)
        elif bt_discard:
            process_annotation(using_sqs_queue, filename, 'discarded image', session)


def get_next_sqs_message():
    messages = sqs_client.receive_message(QueueUrl=sqs_queue_url, MaxNumberOfMessages=1,
                                          WaitTimeSeconds=1)
    if 'Messages' in messages:
        return messages['Messages'][0]
    return None


def delete_sqs_message(message):
    result = sqs_client.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=message['ReceiptHandle'])
    return result['ResponseMetadata']['HTTPStatusCode'] == 200


def process_annotation(using_sqs_queue, filename, pet_type, session):
    save_to_database(filename, pet_type)
    if using_sqs_queue and not delete_sqs_message(session.message_value):
        st.error('Error in deleting message!')
    reset_session(session)


def save_to_database(filename, pet_type):
    try:
        db.insert_into_db(db.AnnotationPets(filename=filename, pet_type=pet_type))
    except exc.IntegrityError:
        db.update_db(db.AnnotationPets, {'filename': filename}, {'pet_type': pet_type,
                                                                 'annotated_at': datetime.utcnow()})


def reset_session(session):
    session.message_value = None
    raise RerunException(RerunData(widget_state=None))


if __name__ == '__main__':
    main()

import os
from typing import Optional

from confluent_kafka import Producer, Consumer, KafkaError, KafkaException

class KafkaConnector:
    def __init__(self):
      self.config = {
        'bootstrap.servers': os.getenv("KAFKA_SERVER")
      }

    def error_callback(self, err: KafkaError):
        print(str(err))
        #   raise ServiceException(err.str())

    def __get_producer(self) -> Producer:
      return Producer({ 
        **self.config,
        'retries': 0, 
        'error_cb': self.error_callback 
      })

    def produce(self, topic, message):
      producer = self.__get_producer()
      producer.produce(topic, message)
      producer.flush()

    def __get_consumer(self, group_id, topics) -> Consumer:
      try:
        consumer = Consumer({ 
            **self.config, 
            'group.id': group_id,
            'enable.auto.commit': True,
            'auto.offset.reset': os.getenv("KAFKA_AUTO_OFFSET"),
            'session.timeout.ms': 6000
        })
        consumer.subscribe(topics)
        return consumer
      except KafkaException as err:
        print('Error while consuming message ' + str(err))
        # raise ServiceException(f'Error while consuming message: "{err.args[0].str()}."')
    
    def consume(self, group_id: str, topic: str, timeout=10.0):
      consumer = self.__get_consumer(group_id, [topic])
      msg = consumer.poll(timeout) # Pull a message takes as much as 10 seconds
      consumer.close() # Close the consumer 
      if msg is None:
        print('Error consuming a message that does not have a message part.')
        # raise ServiceException('Error consuming a message that does not have a message part.')
      elif not msg.error():
        return msg.value().decode('utf-8')
      elif msg.error().code() == KafkaError._PARTITION_EOF:
        print(str(err))
        # raise ServiceException(f'End of partition reached {msg.topic()}/{msg.partition()}.')
      else:
        print('Error while consuming message')
        # raise ServiceException(f'Error while consuming message: {(msg.error().str())}.')

class KafkaConsumer:
  def __init__(self):
    self.connector = KafkaConnector()

  def consume(self, consumer: Consumer):
    action = 'consume'
    print(f'I:--START--:--{action}--')

    try:
      msg = self.connector.consume(consumer.group_id, consumer.topic, conf=consumer.config)
      print(f'O:--SUCCESS--:--{action}--:msg/{msg}')
      return msg
    except Exception as err:
      self.__handle_error(action, err)

  def __handle_error(self, action, err):
    print("Error: " + str(err))
    # dir(err)
    # desc = MessageCode.UNKNOWN_ERROR.value if len(err.args) == 0 else err.args[0]
    # print(f'O:--FAIL--:--{action}--:errorDesc/{desc}')
    # raise ServiceException(desc)

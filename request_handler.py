import requests
import base64
import threading
import time
import sys
import cv2


def decode_image(image_path):
    img_bgr = cv2.imread(image_path)  # BGR Image
    image_data = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # RGB Image
    img_encoded = cv2.imencode('.jpg', image_data)[1]
    return base64.b64encode(img_encoded).decode()


def create_request_handler(
        url,
        response_flag=True):

    handler = RequestHandler()
    handler.project_name = ""
    handler.url = url
    handler.response_flag = response_flag
    handler.thread_times = 1

    return handler


class RequestHandler:
    def __init__(self) -> None:
        # input
        self.project_name = None
        self.url = None
        self.thread_times = None
        self.response_flag = False
        self.image_path_list = None

        # output
        self.return_counter = 0
        self.true_response = 0
        self.false_response = 0
        self.start_time = None
        self.end_time = None
        self.time_elapse = None
        self.average_tps = None
        self.single_response_time = None
        self.max_response_time = None
        self.payload = None
        self.response_time_list = []
        self.response_data_list = []

    def send_request_get(self):
        time_start = time.perf_counter()
        res = requests.get(self.url)
        self.time_elapse = time.perf_counter()-time_start
        self.response_data_list.append(res.text)
        if self.response_flag:
            print(res.text)
        return res.text

    def send_request_post(self, payload):
        if not self.payload:
            print("self.payload is empty")
            return None
        if not self.url:
            print("self.url is empty")
            return None
        time_start = time.perf_counter()
        res = requests.post(self.url, json=self.payload)
        self.time_elapse = time.perf_counter()-time_start
        self.response_data_list.append(res.text)
        if self.response_flag:
            print(res.text)
        return res.text

    def set_url(self, url):
        self.url = url

    def set_payload(self, payload):
        self.payload = payload

    def get_time_elapse(self):
        return self.time_elapse

    def run_thread_process(self):
        function_array = []
        self.start_time = time.perf_counter()
        for i in range(self.thread_times):
            function_array.append(threading.Thread(
                target=self.send_request_post))
            function_array[i].start()

        for i in range(self.thread_times):
            function_array[i].join()
        self.time_elapse = time.perf_counter()-self.start_time

    def send_log_to_file(self):
        # print(self.response_data_list)
        # print(self.response_time_list)
        average_tps = self.return_counter/self.time_elapse
        self.max_response_time = max(self.response_time_list)

        # report format
        result_data = "{},{},{},{}".format(
            self.thread_times,
            self.return_counter,
            self.time_elapse,
            average_tps)
        # export result log
        with open(self.project_name+"_result.txt", mode='a') as export_file:
            export_file.write(result_data + '\n')
        # export response log
        print("test: ", len(self.response_data_list))
        with open(self.project_name+"_response.txt", mode='a') as export_file:
            for data in self.response_data_list:
                print(data)
                export_file.write(data)

        # else:
        #     print("export file name is empty")
        #     print(result_data)

    def read_file(self, file_path):
        result = []
        with open(file_path, 'r') as file:
            data = file.readlines()
            for i in data:
                i = i.strip()
                result.append(i)
        return result


class RequestStructure:
    def __init__(self) -> None:
        pass

    def run_pressure_test(self, handler, thread_times):

        handler.return_counter = 0
        handler.thread_times = thread_times
        function_array = []

        #
        handler.start_time = time.perf_counter()
        for i in range(handler.thread_times):
            function_array.append(threading.Thread(
                target=handler.send_pressure_test_request_post))
            function_array[i].start()

        for i in range(handler.thread_times):
            function_array[i].join()
        handler.time_elapse = time.perf_counter()-handler.start_time

        #
        handler.send_log_to_file()

    def run_request_get(self, handler):
        handler.send_request_get()

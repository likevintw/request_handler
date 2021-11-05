from typing import Text
import request_handler.request_handler as request_handler
import time
import requests
import json
import sys
import os


def create_arnoo_accuracy_tester(
        project_name,
        service_url,
        image_url_list,
        ai_id,
        thread_times,
        headers,
        body,
        monitor=True):
    handler = ArnooTestHandler()
    handler.project_name = project_name
    handler.service_url = service_url
    handler.thread_times = thread_times
    handler.ai_id = ai_id
    handler.image_url_list = image_url_list
    handler.monitor = monitor
    handler.response_data_list = []
    handler.return_counter = 0
    handler.true_response = 0
    handler.false_response = 0
    handler.headers = headers
    handler.body = body
    return handler


def create_arnoo_accuracy_tester_updated(
        project_name,
        service_url,
        ai_id,
        image_url_file_path,
        result_file_path,
        monitor):

    image_url_list = []
    with open(image_url_file_path, mode='r') as import_file:
        import_data = import_file.readlines()
        for i in import_data:
            image_url_list.append(i.strip('\n'))

    if len(image_url_list) == 0:
        sys.exit("{} is empty".format(image_url_file_path))

    headers = {"Content-Type": "application/json"}
    body = {
        "AI-CLASS-ID": [ai_id],
        "ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "TIMESTAMP": "1606358900",
        "PRIVATE-TOKEN": "xxxxxxxxxxxxx",
        "ROI": {},
        "IMAGE":
        {
            "src": "",
            "srcType": "URL",
            "width": 1920,
            "height": 1080,
            "channel": 3,
            "format": "RGB",
            "createTime": "1606358900"
        },
        "DEVICE-INFO":
        {
            "id": "3896965f-6f1e-41c6-8640-70d5d42820ce",
            "location": "26.9839048309, 124.9084309890",
        },
    }

    handler = ArnooTestHandler()
    handler.project_name = project_name
    handler.service_url = service_url
    handler.headers = headers
    handler.body = body
    handler.result_file_path = result_file_path
    handler.image_url_list = image_url_list
    handler.monitor = monitor

    return handler


def create_arnoo_handler(
        project_name,
        url,
        image_url,
        ai_id,
        thread_times,
        response_flag=True):

    handler = ArnooTestHandler()
    handler.project_name = project_name
    handler.url = url
    handler.thread_times = thread_times
    handler.ai_id = ai_id
    handler.image_url = image_url
    handler.response_flag = response_flag
    handler.response_time_list = []
    handler.response_data_list = []
    handler.return_counter = 0
    handler.true_response = 0
    handler.false_response = 0
    return handler


def create_arnoo_handler_20210917(
    project_name,
    service_url,
    ai_id,
    image_url_list_file_path,
    thread_time=1,
    message_flag=True,
):
    handler = ArnooTestHandler()
    handler.project_name = project_name
    handler.service_url = service_url
    handler.ai_id = ai_id
    handler.thread_time = thread_time
    handler.message_flag = message_flag
    handler.image_url_list_file_path = image_url_list_file_path
    handler.headers = {
        "Authorization": "Bearer xxxxx",
        "PRIVATE-TOKEN": "abbcdadafae",
        "Content-Type": "application/json"}
    handler.body = {
        "AI-CLASS-ID": handler.ai_id,
        "ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "TIMESTAMP": "1606358900",
        "PRIVATE-TOKEN": "xxxxxxxxxxxxx",
        "IMAGE":
        {
            "src": "",
            "srcType": "URL",
            "width": 1920,
            "height": 1080,
            "channel": 3,
            "format": "RGB",
            "createTime": "1606358900"
        },
        "DEVICE-INFO":
        {
            "id": "3896965f-6f1e-41c6-8640-70d5d42820ce",
            "location": "26.9839048309, 124.9084309890",

        },
    }
    return handler


def create_arnoo_ROI_accuracy_test_handler_20210917(
    project_name,
    service_url,
    ai_id,
    image_url_ROI_point_json_file_path,
    thread_time=1,
    message_flag=True
):
    handler = ArnooTestHandler()
    handler.project_name = project_name
    handler.service_url = service_url
    handler.ai_id = ai_id
    handler.thread_time = thread_time
    handler.message_flag = message_flag
    handler.image_url_ROI_point_json_file_path = image_url_ROI_point_json_file_path
    handler.headers = {
        "Authorization": "Bearer xxxxx",
        "PRIVATE-TOKEN": "abbcdadafae",
        "Content-Type": "application/json"}
    handler.body = {
        "AI-CLASS-ID": handler.ai_id,
        "ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "TIMESTAMP": "1606358900",
        "PRIVATE-TOKEN": "xxxxxxxxxxxxx",
        "ROI": {},
        "IMAGE":
        {
            "src": "",
            "srcType": "URL",
            "width": 1920,
            "height": 1080,
            "channel": 3,
            "format": "RGB",
            "createTime": "1606358900"
        },
        "DEVICE-INFO":
        {
            "id": "3896965f-6f1e-41c6-8640-70d5d42820ce",
            "location": "26.9839048309, 124.9084309890",

        },
    }
    return handler


def create_arnoo_test_handler_20210914(
    project,
    ai_id,
    service_url,
    ROI_json_path,
    private_token={},
    response_flag=True
):

    handler = ArnooTestHandler()
    handler.ai_id = ai_id
    handler.project = project
    handler.ROI_json_path = ROI_json_path
    handler.url = service_url
    handler.response_flag = response_flag
    handler.response_time_list = []
    handler.response_data_list = []
    handler.return_counter = 0
    handler.true_response = 0
    handler.false_response = 0
    handler.probability = 0
    handler.roi_result = []
    handler.private_token = private_token
    return handler


class ArnooTestHandler (request_handler.RequestHandler):
    def __init__(self) -> None:
        self.project_name = None
        self.ai_id = []
        self.monitor = False
        self.response_flag = None
        self.service_url = []
        self.roi_result = []
        self.project = ""
        self.ROI_json_path = ""
        self.private_token = {}
        self.body = None
        self.message_flag = None
        self.image_url_list = []
        self.thread_time = None
        self.headers = None
        self.image_url_list_file_path = None
        self.image_url_ROI_point_json_file_path = None
        self.response_time_list = []
        self.response_message_list = []
        self.result_file_path = None

    def send_request_post(self):
        self.time_elapse = None
        start_time = time.perf_counter()
        res = requests.post(
            self.service_url, headers=self.headers, json=self.body)
        self.time_elapse = time.perf_counter()-start_time
        try:
            result = json.loads(res.text)
        except:
            self.response_message_list.append(
                "{},No File".format(self.body["IMAGE"]["src"]))

            print(self.headers)
            print(self.body)
            print(res.text)
            return 0

        # if self.monitor:
        #     print(self.headers)
        #     print(self.body)

        # append response time
        self.response_time_list.append("{},{}".format(
            result[0]["IMAGE"]["src"],
            self.time_elapse))

        try:
            if self.monitor:
                print("{},{}".format(
                    result[0]["IMAGE"]["src"],
                    result[0]["OBJECTS"][0]["probability"]
                ))
                # print("time_elapse: ", self.time_elapse)
            # response message
            self.response_message_list.append("{},{}".format(
                result[0]["IMAGE"]["src"],
                result[0]["OBJECTS"][0]["probability"]
            ))
        except:
            if self.monitor:
                print("{},None".format(result[0]["IMAGE"]["src"]))
                # print("time_elapse: ", self.time_elapse)
            # response message
            self.response_message_list.append(
                "{},None".format(result[0]["IMAGE"]["src"]))

    def send_accuracy_test_post_20211105(self, image_url):
        self.body["IMAGE"]["src"] = image_url
        start_time = time.perf_counter()
        res = requests.post(
            self.service_url, headers=self.headers, json=self.body)
        time_elapse = time.perf_counter()-start_time

        # check image file exist
        result = json.loads(res.text)
        if "FLAME-AI" in str(result):
            message = "{},No Image File".format(image_url)
            return message, time_elapse

        # check positive or negative
        try:
            message = "{},{}".format(
                result[0]["IMAGE"]["src"],
                result[0]["OBJECTS"][0]["probability"]
            )
            return message, time_elapse
        except:
            message = "{},False".format(image_url)
            return message, time_elapse

    def send_accuracy_test_post(self, image_url):
        self.body["IMAGE"]["src"] = image_url
        start_time = time.perf_counter()
        res = requests.post(
            self.service_url, headers=self.headers, json=self.body)
        time_elapse = time.perf_counter()-start_time

        try:
            result = json.loads(res.text)
        except:
            message = "{},No Image File".format(image_url)
            return message, time_elapse

        try:
            message = "{},{}".format(
                result[0]["IMAGE"]["src"],
                result[0]["OBJECTS"][0]["probability"]
            )
            return message, time_elapse
        except:
            message = "{},False".format(image_url)
            return message, time_elapse

    def send_threshold_request_post(self, image_url):
        self.body["IMAGE"]["src"] = image_url
        start_time = time.perf_counter()
        res = requests.post(
            self.service_url, headers=self.headers, json=self.body)
        time_elapse = time.perf_counter()-start_time
        try:
            result = json.loads(res.text)
        except:
            message = "{},No Image File".format(image_url)
            return message, time_elapse

        try:
            message = "{},{}".format(
                result[0]["IMAGE"]["src"],
                result[0]["OBJECTS"][0]["probability"]
            )
            return message, time_elapse
        except:
            message = "{},False".format(image_url)
            return message, time_elapse

    def send_ROI_accurace_request_post_20210917(self):

        self.time_elapse = None
        start_time = time.perf_counter()
        res = requests.post(
            self.service_url, headers=self.headers, json=self.body)
        self.time_elapse = time.perf_counter()-start_time

        result = json.loads(res.text)
        # print(self.body)
        print(result)
        try:
            pass
            # for i in result[0][""]
            # print(res.text)
            # print("{},{}".format(
            #     result[0]["IMAGE"]["src"],
            #     result[0]["OBJECTS"][0]["probability"]
            # ))
        except:
            # print("{}, {}".format(result[0]["IMAGE"]["src"], "None"))
            pass

    def check_list_true_element(self, x, y):
        if len(x) != len(y):
            return False
        result = map(lambda x, y: x or y, x, y)
        return list(result)

    def send_ROI_accurace_request_post_20210914(
            self,
            ai_id,  # list, ["3126a0df-bbe8-4e80-b1f2-e7ff9c8dcff6"]
            private_token,  # dict, {"human": 0.60, "pet": 0.5, "vehicle": 0.5}
            image_url,  # string
            project,
            ROI_regions  # {"human":[(0,0,100,100),(100,100,200,200)]}
    ):

        headers = {"Authorization": "Bearer xxxxx",
                   "PRIVATE-TOKEN": "abbcdadafae", "Content-Type": "application/json"}

        body = {
            "AI-CLASS-ID": ai_id,
            "ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "TIMESTAMP": "1606358900",
            "PRIVATE-TOKEN": "xxxxxxxxxxxxx",
            "ROI": {},
            "IMAGE":
            {
                "src": image_url,
            },
            "DEVICE-INFO":
            {
                "id": "3896965f-6f1e-41c6-8640-70d5d42820ce",
            },
        }
        body["ROI"].update({project: ROI_regions})

        # print(self.url)
        # print(body)

        self.probability = 0

        res = requests.post(self.url, headers=headers, json=body)

        # check reponse is empty or not
        try:
            result = json.loads(res.text)
            # print(result[0]["OBJsECTS"])
        # reponse is empty, no image url
        except:
            print("{}, No Image".format(image_url))
            return 0

        # check probability, positive or negative
        try:
            self.probability = result[0]["OBJECTS"][0]["probability"]
            # print("{},{}".format(image_url, self.probability))
        # case probability negative
        except:
            print("{},False".format(image_url))
            return 0

        # check OBJECTS ROI
        try:
            if len(ROI_regions) == 0:
                print("{},has no ROI Data".format(image_url))
                return 0
            roi_result = []
            for i in range(len(ROI_regions)):
                roi_result.append(False)
            x = roi_result
            y = result[0]["OBJECTS"]
            for i in range(len(result[0]["OBJECTS"])):
                roi_result = self.check_list_true_element(
                    roi_result, result[0]["OBJECTS"][i]["roi"])
                if not roi_result:
                    sys.exit("{} is False".format(roi_result))

            for i in range(len(roi_result)):
                print("{}, {}, {}, {}, {}, {}, {}".format(
                    image_url,
                    self.probability,
                    ROI_regions[i][0],
                    ROI_regions[i][1],
                    ROI_regions[i][2],
                    ROI_regions[i][3],
                    roi_result[i]))
        except:
            print("{},ROI Check Error".format(image_url))
            print(x)
            print(y)
            return 0

    def send_ROI_accurace_request_pos(
            self,
            ai_id,  # list, ["3126a0df-bbe8-4e80-b1f2-e7ff9c8dcff6"]
            private_token,  # dict, {"human": 0.60, "pet": 0.5, "vehicle": 0.5}
            image_url,  # string
            project,
            ROI_regions  # {"human":[(0,0,100,100),(100,100,200,200)]}
    ):

        headers = {"Authorization": "Bearer xxxxx",
                   "PRIVATE-TOKEN": "abbcdadafae", "Content-Type": "application/json"}

        body = {
            "AI-CLASS-ID": ai_id,
            "ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "TIMESTAMP": "1606358900",
            "PRIVATE-TOKEN": "xxxxxxxxxxxxx",
            "ROI": {},
            "IMAGE":
            {
                "src": image_url,
            },
            "DEVICE-INFO":
            {
                "id": "3896965f-6f1e-41c6-8640-70d5d42820ce",
            },
        }
        body["ROI"].update({project: ROI_regions})

        # print(self.url)
        # print(body)

        self.probability = 0
        self.roi_result = []
        try:
            res = requests.post(self.url, headers=headers, json=body)
            result = json.loads(res.text)
            self.probability = result[0]["OBJECTS"][0]["probability"]
            self.roi_result = result[0]["OBJECTS"][0]["roi"]
            print(result[0]["IMAGE"]["src"])
            print(result[0]["OBJECTS"][0]["probability"])
            # print("{}, {}".format(
            #     result[0]["IMAGE"]["src"], result[0]["OBJECTS"][0]["probability"]))
            for i in range(len(ROI_regions)):
                # print("{}, {}".format(ROI_regions[i], self.roi_result[i]))
                print("{},{},{},{},{}".format(
                    result[0]["IMAGE"]["src"],
                    ROI_regions[i][0],
                    ROI_regions[i][1],
                    ROI_regions[i][2],
                    ROI_regions[i][3]))
            # print(result)

        except:
            # print("{}, None".format(image_url))
            print("{}".format(image_url))

    def send_mutiple_request_post(self):
        self.time_elapse = None
        start_time = time.perf_counter()
        res = requests.post(
            self.service_url, headers=self.headers, json=self.body)
        self.time_elapse = time.perf_counter()-start_time

        try:
            result = json.loads(res.text)
        except:
            self.response_message_list.append(
                "{},No File".format(self.body["IMAGE"]["src"]))

            print(self.headers)
            print(self.body)
            print(res.text)
            return 0

        # if self.monitor:
        #     print(self.body["AI-CLASS-ID"])
            # print(self.body)
            # print(self.headers)

        # append response time
        self.response_time_list.append("{},{}".format(
            result[0]["IMAGE"]["src"],
            self.time_elapse))

        try:
            if self.monitor:
                # print(result)
                for i in result:
                    for j in i["OBJECTS"]:
                        print("{},{},{}".format(
                            self.body["IMAGE"]["src"], j["class_id"], j["probability"]))
                        # response
                        self.response_message_list.append("{},{},{}".format(
                            self.body["IMAGE"]["src"], j["class_id"], j["probability"]))
        except:
            if self.monitor:
                print("{},None".format(result[0]["IMAGE"]["src"]))
                # print("time_elapse: ", self.time_elapse)
            # response message
            self.response_message_list.append(
                "{},None".format(result[0]["IMAGE"]["src"]))

    def send_log_to_file(self):
        average_tps = self.return_counter/self.time_elapse
        self.max_response_time = max(self.response_time_list)

        # report format
        result_data = "{},{},{},{}".format(
            self.thread_times,
            self.return_counter,
            self.time_elapse,
            average_tps)

        result_log_name = "./pressure_test/{}_result_log.txt".format(
            self.project_name)
        response_log_name = "./pressure_test/{}_response_log.txt".format(
            self.project_name)
        response_time_log_name = "./pressure_test/{}_response_time_log.txt".format(
            self.project_name)

        # export result log
        with open(result_log_name, mode='a') as export_file:
            export_file.write(result_data + '\n')
        # export response log
        with open(response_log_name, mode='a') as export_file:
            export_file.write("====" + str(self.thread_times)+"====" + '\n')
            for data in self.response_data_list:
                export_file.write(data+'\n')
        # export response time log
        with open(response_time_log_name, mode='a') as export_file:
            export_file.write("====" + str(self.thread_times)+"====" + '\n')
            for data in self.response_time_list:
                export_file.write(str(data)+"\n")

    def save_accuracy_log(self):
        # average_tps = self.return_counter/self.time_elapse
        # self.max_response_time = max(self.response_time_list)

        # # report format
        # result_data = "{},{},{},{},{},{}".format(
        #     self.thread_times,
        #     self.return_counter,
        #     self.true_response,
        #     self.false_response,
        #     self.time_elapse,
        #     average_tps)

        # result_log_name = "./accuracy_result/{}_result_log.txt".format(
        #     self.project_name)
        response_message_log_name = "./accuracy_result/{}_response_messgae_log.txt".format(
            self.project_name)
        response_time_log_name = "./accuracy_result/{}_response_time_log.txt".format(
            self.project_name)

        # export result log
        # with open(result_log_name, mode='a') as export_file:
        #     export_file.write("Image Url, Probability")
        #     export_file.write(result_data + '\n')

        # export response log
        with open(response_message_log_name, mode='a') as export_file:
            export_file.write("Image Url, Probability\n")
            for data in self.response_message_list:
                export_file.write(data+'\n')
        # export response time log
        with open(response_time_log_name, mode='a') as export_file:
            export_file.write("Image Url, Time Elapse\n")
            for data in self.response_time_list:
                export_file.write(str(data)+"\n")

    def import_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def set_body(self, body):
        self.body = body

    def count_keyword_number(self, input_list, keyword):
        counter = 0
        for i in input_list:
            if keyword in i:
                counter += 1
        return counter

    def export_txt(self, file_path, list_data):
        with open(file_path, mode='w') as file:
            for data in list_data:
                file.write(data+'\n')


class ArnooRequestStructure():
    def __init__(self) -> None:
        pass

    def run_arnoo_accuracy_test(self, handler):
        if len(handler.image_url_list) == 0:
            exit("{} is empty".format("handler.image_url_list"))

        # test_counter = 0
        for url in handler.image_url_list:
            handler.body.update({"IMAGE": {"src": url}})
            # print(handler.body["IMAGE"]["src"])
            # print(handler.body)
            handler.send_request_post()

            # test_counter += 1
            # if test_counter > 6:
            #     break

        handler.return_counter = len(handler.image_url_list)
        handler.save_accuracy_log()

    def run_arnoo_accuracy_test_1012(self, handler):
        message_list = []
        time_elapse_list = []
        for url in handler.image_url_list:
            message, time_elapse = handler.send_accuracy_test_post_20211105(
                url)
            message_list.append(message)
            time_elapse_list.append(time_elapse)
            if handler.monitor:
                print(message)

        no_image_number = handler.count_keyword_number(
            message_list, "No Image")
        negative_number = handler.count_keyword_number(
            message_list, "False")
        positive_number = len(handler.image_url_list) - \
            no_image_number-negative_number
        message_list.append("Total: {}".format(len(handler.image_url_list)))
        message_list.append("Positive: {}".format(positive_number))
        message_list.append("Negative: {}".format(negative_number))
        message_list.append("No Image: {}".format(no_image_number))
        if handler.monitor:
            print("Total: {}".format(len(handler.image_url_list)))
            print("Positive: {}".format(positive_number))
            print("Negative: {}".format(negative_number))
            print("No Image: {}".format(no_image_number))

        file_path = handler.result_file_path+"/"+handler.project_name+".txt"
        handler.export_txt(file_path, message_list)

    def run_arnoo_accuracy_ROI_test(self, handler):
        data = handler.import_json(handler.ROI_json_path)
        buffer = []
        # counter = 0
        for i in data.keys():
            buffer = []
            for j in data[i]:
                buffer.append(tuple(j))
                if len(buffer) > 4:
                    break

            handler.send_ROI_accurace_request_post_20210914(
                handler.ai_id,
                None,
                i,
                handler.project,
                buffer
            )
            # counter += 1
            # if counter > 10:
            #     break

        # body = {
        #             "AI-CLASS-ID": [self.ai_id],
        #             "ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        #             "TIMESTAMP": "1606358900",
        #             "PRIVATE-TOKEN": "xxxxxxxxxxxxx",
        #             "IMAGE":
        #             {
        #                 "src": self.image_url,
        #                 "srcType": "URL",
        #                 "width": 1920,
        #                 "height": 1080,
        #                 "channel": 3,
        #                 "format": "RGB",
        #                 "createTime": "1606358900"
        #             },
        #             "DEVICE-INFO":
        #             {
        #                 "id": "3896965f-6f1e-41c6-8640-70d5d42820ce",
        #                 "location": "26.9839048309, 124.9084309890",

        #             },
        #         }

    def run_arnoo_threshold_test_backup(self, handler):
        if len(handler.image_url_list) == 0:
            exit("{} is empty".format("handler.image_url_list"))

        # test_counter = 0
        for url in handler.image_url_list:
            # handler.body.update({"IMAGE": {"src": url}})
            # print(handler.body["IMAGE"]["src"])
            # print(handler.body)
            handler.send_threshold_request_post(url)

            # test_counter += 1
            # if test_counter > 6:
            #     break

        handler.return_counter = len(handler.image_url_list)
        handler.save_accuracy_log()

    def run_arnoo_threshold_test(self, handler):
        message_list = []
        time_elapse_list = []
        for url in handler.image_url_list:
            message, time_elapse = handler.send_accuracy_test_post(url)
            message_list.append(message)
            time_elapse_list.append(time_elapse)
            if handler.monitor:
                print(message)

        no_image_number = handler.count_keyword_number(
            message_list, "No Image")
        negative_number = handler.count_keyword_number(
            message_list, "False")
        positive_number = len(handler.image_url_list) - \
            no_image_number-negative_number
        message_list.append("Total: {}".format(len(handler.image_url_list)))
        message_list.append("Positive: {}".format(positive_number))
        message_list.append("Negative: {}".format(negative_number))
        message_list.append("No Image: {}".format(no_image_number))
        if handler.monitor:
            print("Total: {}".format(len(handler.image_url_list)))
            print("Positive: {}".format(positive_number))
            print("Negative: {}".format(negative_number))
            print("No Image: {}".format(no_image_number))

        file_path = handler.result_file_path+"/"+handler.project_name+".txt"
        handler.export_txt(file_path, message_list)

    def run_arnoo_mutiple_test(self, handler):
        if len(handler.image_url_list) == 0:
            exit("{} is empty".format("handler.image_url_list"))

        # test_counter = 0
        for url in handler.image_url_list:
            handler.body.update({"IMAGE": {"src": url}})
            handler.send_mutiple_request_post()

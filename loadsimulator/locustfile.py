from locust import HttpUser, between, task
from requests.auth import HTTPBasicAuth
import random, mechanize, json
import time

class WebsiteUser(HttpUser):
    wait_time = between(1,5)
    @task
    def make_apoitment(self):
        services = []
        providers = []
        resp = self.client.get("/")
        for l in resp.iter_lines():
            splited_line = l.decode().split(":")
            if "availableServices" in splited_line[0] :
                array = "".join([ ":" + x if ind != 0 else x for ind, x in enumerate(splited_line[1:])])[0:-1]
                services = json.loads(array)
            if "availableProviders" in splited_line[0] :
                array = "".join([ ":" + x if ind != 0 else x for ind, x in enumerate(splited_line[1:])])[0:-1]
                providers = json.loads(array)
        self.client.get("/assets/ext/bootstrap/css/bootstrap.min.css?52FX8=")
        self.client.get("/assets/ext/jquery-ui/jquery-ui.min.css?52FX8=")
        self.client.get("/assets/ext/jquery-ui/images/ui-icons_ffffff_256x240.png")
        self.client.get("/assets/ext/jquery-qtip/jquery.qtip.min.css?52FX8=")
        self.client.get("/assets/css/frontend.css?52FX8=")
        self.client.get("/assets/ext/cookieconsent/cookieconsent.min.css?52FX8=")
        self.client.get("/assets/css/general.css?52FX8=")
        self.client.get("/assets/js/general_functions.js?52FX8=")
        self.client.get("/assets/ext/jquery/jquery.min.js?52FX8=")
        self.client.get("/assets/ext/jquery-ui/jquery-ui.min.js?52FX8=")
        self.client.get("/assets/ext/jquery-qtip/jquery.qtip.min.js?52FX8=")
        self.client.get("/assets/ext/cookieconsent/cookieconsent.min.js?52FX8=")
        self.client.get("/assets/ext/bootstrap/js/bootstrap.min.js?52FX8=")
        self.client.get("/assets/ext/datejs/date.js?52FX8=")
        self.client.get("/assets/js/frontend_book_api.js?52FX8=")
        self.client.get("/assets/js/frontend_book.js?52FX8=")
        self.client.get("/assets/ext/bootstrap/fonts/glyphicons-halflings-regular.woff2")

        csrfToken = self.client.cookies.get_dict()["csrfCookie"]
        self.client.get("/assets/img/logo.png?52FX8=")
        self.client.get("/assets/img/favicon.ico?52FX8=")

        service = str(random.choice(services)["id"])

        while(True):
            try: 
                provider = str(random.choice([ p["id"] for p in providers  if service in p["services"] ]))
            except:
                service = str(random.choice(services)["id"])
                continue
            break

        while(True):
            try:
                day = str(random.randint(1,30))
                
                date = "2020-0"+str(random.randint(7,9))+"-"+day if len(day) > 1 else "2020-0"+str(random.randint(7,9))+"-0"+day
                post_data = {
                    "csrfToken" : csrfToken,
                    "service_id":service,
                    "provider_id":provider,
                    "selected_date":date,
                    "service_duration":10,
                    "manage_mode":"false"
                }
                hour = random.choice(self.client.post('/index.php/appointments/ajax_get_available_hours', data=post_data).json())
                self.client.get(f"/index.php/appointments/ajax_get_unavailable_dates?provider_id={provider}&service_id={service}&selected_date={date}&csrfToken={csrfToken}&manage_mode=false", name="/index.php/appointments/ajax_get_unavailable_dates")   
            except:
                time.sleep(5)
                continue
            break

        end_hour = hour.split(":")[0] +":"+ str(int(hour.split(":")[1]) + 10)


        post_data = {
            "csrfToken" : csrfToken,
            "post_data[customer][last_name]" : "sasdasdas",
            "post_data[customer][first_name]" : "asdasdasd",
            "post_data[customer][email]": "asd@ua.pt",
            "post_data[customer][phone_number]" : "123456789",
            "post_data[customer][address]" : "",
            "post_data[customer][city]" : "",
            "post_data[customer][zip_code]" : "",
            "post_data[appointment][start_datetime]" : date +" "+ hour+":00",
            "post_data[appointment][end_datetime]" : date + " "+ end_hour+":00",
            "post_data[appointment][notes]" : "",
            "post_data[appointment][is_unavailable]" : "false",
            "post_data[appointment][id_users_provider]" : provider,
            "post_data[appointment][id_services]": service,
            "post_data[manage_mode]" : "false"
        }
        appointment_id = self.client.post('/index.php/appointments/ajax_register_appointment', data=post_data).json()["appointment_id"]
        time.sleep(5)
        print(appointment_id)
        self.client.get(f"/index.php/appointments/book_success/{appointment_id}", name="/index.php/appointments/book_success")
        self.client.get("/assets/img/success.png")
        self.client.get("/assets/ext/jquery/jquery.min.js")
        self.client.get("/assets/ext/bootstrap/js/bootstrap.min.js")
        self.client.get("/assets/ext/datejs/date.js")
        self.client.get("/assets/js/frontend_book_success.js?52FX8=")
        self.client.get("/assets/ext/bootstrap/css/bootstrap.min.css?52FX8=")
        self.client.get("/assets/css/frontend.css?52FX8=")
        self.client.get("/assets/js/general_functions.js?52FX8=")
        self.client.get("/assets/img/logo.png?52FX8=")
        self.client.get("/assets/img/favicon.ico?52FX8=")
        time.sleep(5)


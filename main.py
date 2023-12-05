import requests
from kivy.app import App
from kivy.uix.recycleview import RecycleView  # Import RecycleView
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
import json

class Menu(BoxLayout):
    pass

class MyRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(MyRecycleView, self).__init__(**kwargs)
        self.load_data()
        Clock.schedule_interval(self.load_data, 1)
    
    def load_data(self, *args):
        store = requests.get('http://127.0.0.1:8000/').json()

        list_data = []
        for item in store:
            list_data.append({'text': item['name']})
        self.data = list_data

class HomeScreen(Screen):
    pass

class AddNewForm(Widget):
    text_input = ObjectProperty(None)
    input = StringProperty('')

    def submit_input(self):
        self.input = self.text_input.text
        post = requests.post('http://127.0.0.1:8000/create', json={'name': self.input})
        self.input = ''

class AddScreen(Screen):
    def __init__(self, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
        self.box = BoxLayout()
        self.box.orientation = "vertical"
        self.box.add_widget(Label(text="Add To List...", color="blue", pos_hint={"top": 1}))
        self.addNewForm = AddNewForm()
        self.box.add_widget(self.addNewForm)
        self.add_widget(self.box)



class UserRegistrationScreen(Screen):
    username_input = ObjectProperty()
    password_input = ObjectProperty()
    email_input = ObjectProperty()

    def register_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        email = self.email_input.text

        if username and password and email:
            data = {
                'username': username,
                'password': password,
                'email': email
            }
            response = requests.post('http://127.0.0.1:8000/users/register/', json=data)

            if response.status_code == 201:
                print('User registered successfully!')
                if hasattr(self, 'manager') and isinstance(self.manager, ScreenManager):
                    print(f'Current screen: {self.manager.current}')
                    self.manager.current = 'screen_login'
                    print(f'Switched to login screen. Current screen: {self.manager.current}')
                else:
                    print('No manager or invalid manager instance.')
            else:
                print('Registration failed.')
                # Handle the failure scenario, such as displaying an error message

class LoginScreen(Screen):
    def on_success(self, req, result):
        # Handle the successful response from the API or local logic
        print('Login successful')
        # Add code to switch to the home screen or desired screen
        # Example: self.manager.current = 'screen_home'

    def on_failure(self, req, result):
        # Handle the failure response from the API or local logic
        print('Invalid username or password')
        # Display an error message or handle accordingly
    def login_user(self):
        username = self.username_input.text
        password = self.password_input.text

        if username and password:
            # Replace 'your_api_url' with the actual URL of your Django API endpoint
            api_url = 'http://127.0.0.1:8000/users/login/'

            # Data to be sent to the Django API
            data = {'username': username, 'password': password}

            # Send a POST request to the Django API
            response = requests.post(api_url, json=data)

            if response.status_code == 200:
                # Handle successful login
                self.on_success(None, response.json())
            elif response.status_code == 401:
                # Handle unsuccessful login
                self.on_failure(None, response.json())
            else:
                # Handle other response statuses
                print(f'Unexpected response status: {response.status_code}')
        else:
            print('Invalid username or password')
            # Display an error message or handle accordingly


class ScreenManagement(ScreenManager):
    pass

class TodoApp(App):
    pass

if __name__ == '__main__':
    TodoApp().run()

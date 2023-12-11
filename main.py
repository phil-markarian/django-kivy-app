import requests
from kivy.lang import Builder
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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
import json

class Menu(BoxLayout):
    pass



class MyRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(MyRecycleView, self).__init__(**kwargs)
        self.load_data()

    def load_data(self):
        store = requests.get('http://127.0.0.1:8000/').json()

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for item in store:
            label = Label(text=item['name'], size_hint_y=None, height=40)
            layout.add_widget(label)

        # Set the layout as the only child of the RecycleView
        self.data = [{'viewclass': 'MyLabel', 'label': label} for label in layout.children]

class MyLabel(Label):
    pass


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

        # Assuming your response JSON contains a 'token' field
        token = result.get('token', '')
        print(token)

        # Set the token in the app
        app = App.get_running_app()
        app.token = token

        # Switch to the user profile screen and pass the token
        screen_manager = app.root.ids.screen_manager
        screen_profile = screen_manager.get_screen('screen_profile')
        screen_profile.set_token(token)  # Call set_token to pass the token
        screen_manager.current = 'screen_profile'

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
                print(response)
                print(f'Unexpected response status: {response.status_code}')
        else:
            print('Invalid username or password')
            # Display an error message or handle accordingly

class UserProfileScreen(Screen):
    username_label = ObjectProperty()
    email_label = ObjectProperty()
    token = ''  # Initialize the token as an empty string

    def set_token(self, token):
        self.token = token
        print(f'Token set in UserProfileScreen: {self.token}')  # Add this line to check if the token is set

    def on_pre_enter(self, *args):
        try:
            # Fetch user profile information
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get('http://127.0.0.1:8000/users/profile/', headers=headers)

            # Check if the request was successful (status code 200)
            if response.ok:
                user_profile_data = response.json()
                username = user_profile_data.get('username', '')
                email = user_profile_data.get('email', '')

                # Display user profile information
                user_profile_label_text = f"User Profile\nUsername: {username}\nEmail: {email}"
                self.username_label.text = f'Username: {username}'
                self.email_label.text = f'Email: {email}'
            else:
                # Handle unsuccessful API response
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            # Handle exceptions (network error, JSON parsing error, etc.)
            print(f"An error occurred: {e}")



class ScreenManagement(ScreenManager):
    pass

class TodoApp(App):
    token = ''  # Initialize the token as an empty string

    def on_success_login(self, req, result):
        # Handle successful login
        print('Login successful')
        self.token = result.get('token', '')  # Get the token from the response
        print(f'Token set: {self.token}')  # Add this line to check if the token is set
        # Add code to switch to the home screen or desired screen
        # Example: self.root.ids.screen_manager.current = 'screen_home'

        # Switch to the user profile screen and pass the token
        screen_manager = self.root.ids.screen_manager
        screen_profile = screen_manager.get_screen('screen_profile')
        screen_profile.set_token(self.token)

    def on_failure_login(self, req, result):
        # Handle unsuccessful login
        print('Invalid username or password')
        # Display an error message or handle accordingly

    def login_user(self, username, password):
        if username and password:
            # Replace 'your_api_url' with the actual URL of your Django API endpoint
            api_url = 'http://127.0.0.1:8000/users/login/'

            # Data to be sent to the Django API
            data = {'username': username, 'password': password}

            # Send a POST request to the Django API
            req = UrlRequest(api_url, on_success=self.on_success_login, on_failure=self.on_failure_login, req_body=json.dumps(data))
        else:
            print('Invalid username or password')
            # Display an error message or handle accordingly

    def on_pre_enter_screen_profile(self, *args):
        try:
            # Fetch user profile information
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get('http://127.0.0.1:8000/users/profile/', headers=headers)

            # Check if the request was successful (status code 200)
            if response.ok:
                user_profile_data = response.json()
                username = user_profile_data.get('username', '')
                email = user_profile_data.get('email', '')

                # Access the UserProfileScreen instance and set the labels
                screen_profile = self.root.ids.screen_manager.get_screen('screen_profile')
                screen_profile.ids.username_label.text = f'Username: {username}'
                screen_profile.ids.email_label.text = f'Email: {email}'

            else:
                # Handle unsuccessful API response
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            # Handle exceptions (network error, JSON parsing error, etc.)
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    TodoApp().run()

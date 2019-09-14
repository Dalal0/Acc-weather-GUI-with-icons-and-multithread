import requests
from tkinter import *
from bs4 import BeautifulSoup
from threading import  Thread
from io import BytesIO
from PIL import ImageTk, Image

class gui(Tk):
    def __init__(self):
        Tk.__init__(self)

        # title of app
        self.title('AccWeather')
        self.geometry('600x500')

        # API
        self.api = 'cKh5lrrqb7L26PC9OFyuj1S1y14oPMCh'

        # main canvas with image
        url = 'https://images.unsplash.com/photo-1451154488477-d20dee2a4e46?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=753&q=80'
        image = requests.get(url).content
        self.img = ImageTk.PhotoImage(Image.open(BytesIO(image)))
        self.main = Label(self, image=self.img)
        self.main.place(relx=.0, rely=.0, relwidth=1, relheight=1)




        # button and input
        self.city = Entry(self.main, bd=0, font=3, fg='black')
        self.city.place(relx=0.1, rely=0.1, relheight=0.1, relwidth=0.6)
        Button(self.main, text='Get Weather', bg='DodgerBlue',font=5, bd=1, command=self.get_weather_call).place(relx=0.7, rely=.1, relheight=0.1,relwidth=0.2)

        # API box
        Label(self.main, bg='white', text='API key: ').place(relx=0.1, rely=0)
        self.api_box = Entry(self.main, bd=1, font=2)
        self.api_box.place(relx=0.2, rely=0, relwidth=.7)
        self.api_box.insert(0, self.api)


        # output label
        Label(self.main, text='OUTPUT:', fg='black',bg='white', font=5).place(relx=.1, rely=.3)
        # output box
        self.put_out = Label(self.main, font=20, anchor='nw', bg='white', justify='left', bd=5)  # border = bd
        self.put_out.place(relx=.1, rely=.4, relwidth=.8, relheight=.5)


        # weather icon
        self.icon = Label(self.main, height=200, width=200, bg='white')
        self.icon.place(relx=.6, rely=.4, relwidth=.3, relheight=.3)


    def get_weather_call(self):
        city = self.city.get()
        thread = Thread(target=self.get_weather, args=(city,))
        thread.start()


    def get_weather(self, city):
        # autocomplete location
        try:
            auto_url = f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={self.api}&q=" + city
            data = requests.get(auto_url).json()

            if [True for i in data.items() for a in i if a=='Unauthorized']:
                self.put_out['text'] = 'Error: '+data['Message']
            else:
                try:
                    key = data[0]['Key']
                    city_name = ', '.join([data[0]['LocalizedName'], data[0]['Country']['LocalizedName']])
                    api = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/{key}?apikey={self.api}").json()

                    temp = api[0]['Temperature']['Metric']['Value']
                    self.text = api[0]['WeatherText']
                    weather = f'City: {city_name}\nTemperature (c): {int(temp)}\nCondition: {self.text}'
                    self.put_out['text'] = weather

                    # get icon
                    thread_weather_icon = Thread(target=self.weather_icon, args=(self.text,))
                    thread_weather_icon.start()

                except Exception as e:
                    self.put_out['text'] = e
        except Exception as e:
            self.put_out['text'] = e

    def weather_icon(self, txt):
        split = txt.split(' ')
        get_text = '+'.join(split)
        url = 'https://www.iconfinder.com/search/?q='+get_text
        req = requests.get(url).content
        soup = BeautifulSoup(req, 'html.parser')
        img_url = soup.find('img', {'class': 'd-block'})['src']
        image_content = requests.get(img_url).content
        self.photo = ImageTk.PhotoImage(Image.open(BytesIO(image_content)))
        self.icon['image'] = self.photo



if __name__ == '__main__':
    start = gui()
    start.mainloop()
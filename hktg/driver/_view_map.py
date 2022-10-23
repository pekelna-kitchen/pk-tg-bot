
from telegram import Update
from telegram.ext import ContextTypes
from dataclasses import dataclass

from enum import Enum
from datetime import datetime

import folium
from folium.plugins import MeasureControl
from html2image import Html2Image
from geopy.geocoders import Nominatim

from hktg.constants import (
    Action,
    State
)
from hktg import db , util, home

KH_CENTER=[49.9989, 36.2473]

@dataclass
class ViewMap:

    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup


        geolocator = Nominatim(user_agent="pekelna-kitchen-bot")
        # location = geolocator.geocode("Харків Амосова 1")
        # print(location.address)

        m = folium.Map(
            location=KH_CENTER,
            zoom_start=12,
            control_scale=True,
            png_enabled=True
        )

        civils = db.get_table(db.Civil)
        locations = []
        for c in civils:
            civil = db.Civil(*c)
            coords = civil.coords()
            if coords:
                locations.append((float(coords.latitude), float(coords.longitude)))
            else:
                location = geolocator.geocode(civil.address)
                locations.append((location.latitude, location.longitude))
            m.add_child(folium.Marker(
                locations[-1],
                popup=civil.address,
            ))

        m.add_child(folium.LatLngPopup())
        m.add_child(MeasureControl())
        m.add_child(folium.vector_layers.PolyLine(
                        locations,
                        # color=random_color,
                        tooltip="hello"
                    ))


        # html = m._repr_html_() 
        html = m.save('index.html')
        hti = Html2Image()
        hti.screenshot(html_file='index.html', save_as='page.png', size=[1280, 720])


        buttons = []
        buttons.append([util.action_button(Action.BACK),])
        keyboard = InlineKeyboardMarkup(buttons)

        from telegram.constants import ParseMode

        await update.effective_message.reply_document(
            open('index.html', 'rb'),
            # 'index.html',
            thumb=open('page.png', 'rb'),
            parse_mode=ParseMode.HTML
        )
        text = "babooshki"
        if update.callback_query:
            # await update.callback_query.pin_message()
            await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=text, reply_markup=keyboard)

        return State.VIEWING_MAP

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        query_data = update.callback_query.data
        # user_data = context.user_data['data']

        if isinstance(query_data, Action):
            return await home.Home.ask(update, context)

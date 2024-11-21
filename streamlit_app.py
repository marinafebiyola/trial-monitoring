import streamlit as st
import requests
import matplotlib.pyplot as plt
import time
import os
import numpy as np
import pandas as pd
from datetime import datetime


st.set_page_config(page_title="Monitoring-kki-2024", page_icon="🌍", layout="wide")

# Backend URL
FLASK_URL = 'http://127.0.0.1:5000/data-receive'
def data_backend():
    try:
        response = requests.get(FLASK_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error: {e}")
        return None
    
#sidebar
st.sidebar.markdown('<h4 class="sidebar-text">NAVIGASI LINTASAN</h4>', unsafe_allow_html=True)
path = st.sidebar.radio("", ["Lintasan A ⚓", "Lintasan B ⚓"])
start_monitoring_button = st.sidebar.button("START BUTTON", key="start_monitoring_button")

#Header
col1, col2, col3, col4 = st.columns([1,4,4,1])
with col1:
    st.image('Images/logo.jpeg', width=75)
with col2:
    st.markdown("<h6 class='header-text'> BARELANG MARINE ROBOTICS TEAM </h6>", unsafe_allow_html=True)
with col3:
    st.markdown("<h6 class='header-text'> POLITEKNIK NEGERI BATAM </h6>", unsafe_allow_html=True)
with col4:
    st.image('Images/polibatamLogo.jpeg', width=80)

#lintasan
if path == "Lintasan A ⚓":
    st.markdown("<h5 class='judul-text'>LINTASAN A</h5>", unsafe_allow_html=True)
elif path == "Lintasan B ⚓":
    st.markdown("<h5 class='judul-text'>LINTASAN B</h5>", unsafe_allow_html=True)

#Informasi geo-tag info
st.markdown("<h6 class='judul-text'>GEO-TAG INFO</h6>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    day_placeholder = col1.metric("Day", "Loading...")
with col2:
    date_placeholder = col2.metric("Date", "Loading...")
with col3:
    time_placeholder = col3.metric("Time", "Loading...")
with col4:
    position_placeholder = col4.metric("Position [x,y]", "Loading...") 
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    sog_knot_placeholder = col1.metric("Coordinate", "Loading...")
with col2:
    sog_kmh_placeholder = col2.metric("SOG [Knot]", "Loading...")
with col3:
    coordinate_placeholder = col3.metric("SOG [Km/h]", "Loading...")
with col4:
    cog_placeholder = col4.metric("COG", "Loading...")

#Position-log
st.markdown("<h6 class='judul-text'>POSITION-LOG</h6>", unsafe_allow_html=True)
table_placeholder = st.empty()    
   
#Trajectory Map
st.markdown("<h5 class='judul-text'>TRAJECTORY MAP</h5>", unsafe_allow_html=True)
def koordinat_kartesius(path):
    fig, ax = plt.subplots(figsize=(13, 13))
    ax.set_xlim(0, 2500)
    ax.set_ylim(0, 2500)
    ax.set_xticks(range(0, 2600, 100))
    ax.set_yticks(range(0, 2600, 100))
    ax.grid(True)
   
    if path == "Lintasan A ⚓":
        #Titik nol : x = 2185, y = 115
        rectangle = plt.Rectangle((2100, 65), 170, 100, color='red', fill=True)
        red_positions, green_positions = posisi_floating_ball("A")

        rectangle = plt.Rectangle((2100, 65), 170, 100, color='red', fill=True)
        ax.add_patch(rectangle)

        blue_rectangle = plt.Rectangle((520, 300), 100, 50, color='blue', fill=True)
        ax.add_patch(blue_rectangle)

        small_green_rectangle = plt.Rectangle((300, 620), 100, 50, color='green', fill=True)
        ax.add_patch(small_green_rectangle)

    elif path == "Lintasan B ⚓":
        #Titik nol : x = 335, y = 115
        rectangle = plt.Rectangle((250, 65), 170, 100, color='green', fill=True)
        red_positions, green_positions = posisi_floating_ball("B")
        
        rectangle = plt.Rectangle((250, 65), 170, 100, color='green', fill=True)
        ax.add_patch(rectangle)

        blue_rectangle = plt.Rectangle((1880, 300), 100, 50, color='blue', fill=True)
        ax.add_patch(blue_rectangle)

        small_green_rectangle = plt.Rectangle((2100, 620), 100, 50, color='green', fill=True)
        ax.add_patch(small_green_rectangle)
    else:
        gambar_lintasan_lomba()
        return None, None

    ax.add_patch(rectangle)
    for pos in red_positions:
        ax.add_patch(plt.Circle(pos, 25, color='red', fill=True))
    for pos in green_positions:
        ax.add_patch(plt.Circle(pos, 25, color='green', fill=True))

    return fig, ax

def posisi_floating_ball(path):
    if path == "A":
        green_positions = [(330, 960), (330, 1310), (450, 1715), (1040, 2250), (1200, 2250),
                         (1360, 2250), (1520, 2250), (2325, 1465), (2180, 1160), (2260, 855)]
        red_positions = [(180, 960), (180, 1310), (300, 1715), (1040, 2100), (1200, 2100),
                           (1360, 2100), (1520, 2100), (2175, 1465), (2030, 1160), (2110, 855)]
    elif path == "B":
        red_positions = [(390, 855), (470, 1160), (325, 1465), (980, 2100), (1140, 2100),
                         (1300, 2100), (1460, 2100), (2200, 1715), (2320, 1310), (2320, 960)]
        green_positions = [(240, 855), (320, 1160), (175, 1465), (980, 2250), (1140, 2250),
                           (1300, 2250), (1460, 2250), (2050, 1715), (2170, 1310), (2170, 960)]
    return red_positions, green_positions

def hasil_foto_surface():
    surface_dir = os.path.expanduser("~/kki2024_ws/surface_box")
    surface_file = "sbox_1.jpg"
    surface_path = os.path.join(surface_dir, surface_file)
    
    if os.path.isfile(surface_path):

        with image_placeholder.container():
            col1, _ = st.columns([1, 1])
            with col1:
                st.markdown("<h6 class='judul-text'>Water Surface Picture</h6>", unsafe_allow_html=True)
                st.image(surface_path, caption="Green Box", use_column_width=True)

        
def hasil_foto_underwater():
    underwater_dir = os.path.expanduser("~/kki2024_ws/underwater_box")
    underwater_file = "ubox_1.jpg"  
    underwater_path = os.path.join(underwater_dir, underwater_file)
    
    if os.path.isfile(underwater_path):
        with image_placeholder.container():
            _, col2 = st.columns([1, 1])
            with col2:
                st.markdown("<h6 class='judul-text'>Under Water Picture</h6>", unsafe_allow_html=True)
                st.image(underwater_path, caption="Blue Box", use_column_width=True)
    else:
        return None, None

def gambar_lintasan_lomba():
    col1, col2 = st.columns(2)
    with col1:
        st.image('Images/lintasanA.jpeg', caption='Lintasan A')
    with col2:
        st.image('Images/lintasanB.jpeg', caption='Lintasan B')

#Visualisasi arah hadap kapal
triangle_patch = None
def heading_kapal(ax, x, y, yaw):
    global triangle_patch

    if triangle_patch is not None:
        triangle_patch.remove() 
        triangle_patch = None

    if yaw > 0:
        yaw = 360 - yaw

    angle = np.deg2rad(yaw) + np.pi / 2
    arrow_length = 35
    base_length = 40

    tip_x = x + arrow_length * np.cos(angle)
    tip_y = y + arrow_length * np.sin(angle)

    left_x = tip_x - base_length * np.cos(angle + np.pi / 6)  
    left_y = tip_y - base_length * np.sin(angle + np.pi / 6) 
    right_x = tip_x - base_length * np.cos(angle - np.pi / 6)  
    right_y = tip_y - base_length * np.sin(angle - np.pi / 6) 

    triangle = np.array([[tip_x, tip_y], [left_x, left_y], [right_x, right_y]])
    triangle_patch = ax.fill(triangle[:, 0], triangle[:, 1], color='darkviolet', alpha=1)[0]
    
    ax.figure.canvas.draw()

plot_placeholder = st.empty()

image_placeholder = st.empty()

fig, ax = koordinat_kartesius(path)

#Update data
table_entries = [] 
trajectory_x = []
trajectory_y = []
floating_ball_count = 0
trajectory_line, = ax.plot([], [], color='black', linestyle='--', marker='o', markersize=1)
finished = False
def update_plot():
    global trajectory_x, trajectory_y, floating_ball_count, finished
    data = data_backend()
    
    if data:
        surface_imaging_executed = False
        underwater_imaging_executed = False
        try:
            
            if path == "Lintasan B ⚓":
                x = data.get('x') + 335
                y = data.get('y') + 115
                
            else:
                x = data.get('x') + 2185
                y = data.get('y') + 115
                # y = data.get('y') + 300

            nilai_x = data.get('x')
            nilai_y = data.get('y')
            knot = data.get('sog_knot')
            km_per_hours = data.get('sog_kmh')
            cog = data.get('cog')
            day = data.get('day')
            date = data.get('date')
            time_value = data.get('time')
            latt = data.get('coordinate1')
            lon = data.get('coordinate1')
            yaw = data.get('yaw')
            time_value = data.get('time')
        
            trajectory_x.append(x)
            trajectory_y.append(y)
            trajectory_line.set_data(trajectory_x, trajectory_y)
            heading_kapal(ax, x, y, yaw)
            plot_placeholder.pyplot(fig)

            sog_knot_placeholder.metric("SOG [Knot]", f"{knot} knot")
            sog_kmh_placeholder.metric("SOG [Km/h]", f"{km_per_hours} km/h")
            cog_placeholder.metric("COG", f"{cog}°")
            day_placeholder.metric("Day", day)
            date_placeholder.metric("Date", date)
            time_placeholder.metric("Time", time_value)
            coordinate_placeholder.metric("Coordinate", f" S{latt}  E{lon}")
            position_placeholder.metric("Position [x,y]",f"{nilai_x}, {nilai_y}")

            if path == "Lintasan A ⚓":
                #set ke-1
                if x >  1800 and y > 900 and floating_ball_count == 0:
                    floating_ball_count = 1
                elif x > 1800 and y > 1200 and floating_ball_count == 1:
                    floating_ball_count = 2
                elif x > 1800 and y > 1500 and floating_ball_count == 2:
                    floating_ball_count = 3
                #set ke-2
                elif y > 1800 and x < 1500 and floating_ball_count == 3:
                    floating_ball_count = 4
                elif y > 1800 and x < 1330 and floating_ball_count == 4:
                    floating_ball_count = 5
                elif y > 1800 and x < 1160 and floating_ball_count == 5:
                    floating_ball_count = 6
                elif y > 1800 and x < 1000 and floating_ball_count == 6:
                    floating_ball_count = 7
                #set ke-3
                elif x < 700 and y < 1690 and floating_ball_count == 7:
                    floating_ball_count = 8
                elif x < 700 and y < 1290 and floating_ball_count == 8:
                    floating_ball_count = 9
                elif x < 700 and y < 920 and floating_ball_count == 9:
                    floating_ball_count = 10
                    
            elif path == "Lintasan B ⚓":
                #set ke-1
                if x < 700 and y > 890 and floating_ball_count == 0:
                    floating_ball_count = 1
                elif x < 700 and y > 1200 and floating_ball_count == 1:
                    floating_ball_count = 2
                elif x < 700 and y > 1500 and floating_ball_count == 2:
                    floating_ball_count = 3
                #set ke-2
                elif y > 1800 and x > 1000 and floating_ball_count == 3:
                    floating_ball_count = 4
                elif y > 1800 and x > 1170 and floating_ball_count == 4:
                    floating_ball_count = 5
                elif y > 1800 and x > 1330 and floating_ball_count == 5:
                    floating_ball_count = 6
                elif y > 1800 and x > 1500 and floating_ball_count == 6:
                    floating_ball_count = 7
                #set ke-3
                elif x > 1800 and y < 1690 and floating_ball_count == 7:
                    floating_ball_count = 8
                elif x > 1800 and y < 1290 and floating_ball_count == 8:
                    floating_ball_count = 9
                elif x > 1800 and y < 920 and floating_ball_count == 9:
                    floating_ball_count = 10

            df = pd.DataFrame(table_entries)
            table_placeholder.dataframe(df, use_container_width=True)

            surface_imaging_executed = False
            underwater_imaging_executed = False
            floating_ball_executed = False

            #Position-log
            if not finished:
                if nilai_x == 0 and nilai_y == 0:
                    event = "Start"
                    entry = {
                        'Day': day,
                        'Date': date,
                        'Time': time_value,
                        'Coordinate': f"S{latt}, E{lon}",
                        'SOG [Knot]': f"{knot} knot",
                        'SOG [Km/h]' : f"{km_per_hours} km/h",
                        'COG': f"{cog}°",
                        'Floating Ball': f"{floating_ball_count}",
                        'Event': event
                    }
                    table_entries.append(entry)
                    return True  
                
                #kondisi untuk mission surface imaging   
                surface_dir = os.path.expanduser("~/kki2024_ws/surface_box")
                surface_file = "sbox_1.jpg"
                surface_path = os.path.join(surface_dir, surface_file)
                if os.path.isfile(surface_path):
                    event = "Mission Surface Imaging"
                    entry = {
                        'Day': day,
                        'Date': date,
                        'Time': time_value,
                        'Coordinate': f"S{latt}, E{lon}",
                        'SOG [Knot]': f"{knot} knot",
                        'SOG [Km/h]' : f"{km_per_hours} km/h",
                        'COG': f"{cog}°",
                        'Floating Ball': f"{floating_ball_count}",
                        'Event': event
                    }
                    table_entries.append(entry)
                    surface_imaging_executed = True

                #kondisi untuk mission underwater imaging   
                underwater_dir = os.path.expanduser("~/kki2024_ws/underwater_box")
                underwater_file = "ubox_1.jpg" 
                underwater_path = os.path.join(underwater_dir, underwater_file)
                if os.path.isfile(underwater_path):
                    event = "Mission Underwater Imaging"
                    entry = {
                        'Day': day,
                        'Date': date,
                        'Time': time_value,
                        'Coordinate': f"S{latt}, E{lon}",
                        'SOG [Knot]': f"{knot} knot",
                        'SOG [Km/h]' : f"{km_per_hours} km/h",
                        'COG': f"{cog}°",
                        'Floating Ball': f"{floating_ball_count}",
                        'Event': event
                    }
                    table_entries.append(entry)
                    underwater_imaging_executed = True

                #kondisi untuk event Finish
                if (path == "Lintasan A ⚓" and x > 2100 and y < 165) or (path == "Lintasan B ⚓" and x < 415 and y < 165):
                    if surface_imaging_executed and underwater_imaging_executed:
                        event = "Finish"
                        entry = {
                            'Day': day,
                            'Date': date,
                            'Time': time_value,
                            'Coordinate': f"S{latt}, E{lon}",
                            'SOG [Knot]': f"{knot} knot",
                            'SOG [Km/h]' : f"{km_per_hours} km/h",
                            'COG': f"{cog}°",
                            'Floating Ball': f"{floating_ball_count}",
                            'Event': event
                        }
                        table_entries.append(entry)
                        finished = True
                        return True 

                if 1 <= floating_ball_count < 10 and not floating_ball_executed:
                    #Kondisi untuk event Floating Ball
                    event = "Floating Ball"
                    entry = {
                        'Day': day,
                        'Date': date,
                        'Time': time_value,
                        'Coordinate': f"S{latt}, E{lon}",
                        'SOG [Knot]': f"{knot} knot",
                        'SOG [Km/h]' : f"{km_per_hours} km/h",
                        'COG': f"{cog}°",
                        'Floating Ball': f"{floating_ball_count}",
                        'Event': event
                    }
                    table_entries.append(entry)
                    floating_ball_executed = True
                    return True

  
        except (TypeError, KeyError) as e:
            st.error(f"Error processing data: {e}")
    else:
        st.warning("No data received.")

# Main loop
if start_monitoring_button:
    st.session_state.monitoring_active = True
    st.sidebar.markdown('<style>div.stButton > button {background-color: #2E7431; color: white;}</style>', unsafe_allow_html=True)
    st.text("Monitoring started...")
    while True:
        update_plot()
        hasil_foto_surface()
        hasil_foto_underwater()
        time.sleep(0.5)       
else:
    gambar_lintasan_lomba()

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-color: #b2d3eb;
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("""
    <style>
        .header-text {
            text-align: center;
            color: #ffff;
            background-color: #3A6E8F;
            padding: 15px; 
            border-radius: 15px;
            margin-bottom: 1px; 
            border: 2px solid white;
            font-size: 16px;
            font-family: 'Montserrat', sans-serif;

        }
        .judul-text {
            text-align: center;
            color: white;
            background-color: #65A7D3;
            padding: 5px; 
            border-radius: 10px;
            margin-bottom: 5px; 
            border: 2px solid white;
            font-size: 14px;
            font-family: 'Montserrat', sans-serif;

        }
        [data-testid="stMetricValue"] {
            font-size: 16px;
            color : #242649;
            font-family: 'Montserrat', sans-serif;
            font-weight: bold; 

        }
        [data-testid="stMetricLabel"] {
            font-size: 12px;
            color : black;
            font-family: 'Montserrat', sans-serif;
        }
        .stButton > button {
            background-color: #4CAF50; 
            color: #ffff;    
            border: 2px solid white;
            font-weight: bold; 
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .sidebar-text {
            text-align: center;
            color: #FFFF;
            background-color: #3A6E8F;
            padding: 10px; 
            border-radius: 15px;
            border: 2px solid white;
            font-size: 12px;
            font-family: 'Montserrat', sans-serif;
        }
        [data-testid="stSidebar"] {
            background-color: #7FBADC;
            color: #ffff;
            font-weight: bold;
            font-family: 'Montserrat', sans-serif; 
        }
    </style>
    """, 
    unsafe_allow_html=True
)
    

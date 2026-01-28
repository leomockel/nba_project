🏀 NBA Project

A set of various project I've done on the theme of NBA. 
In my first formation in a bootcamp of Vivadata (Artefact School of data), I've made a final data project around NBA. From this first idea, several extension have come after.


🚀 The beginning (Bootcamp)

First, I've collected my data with the nba_api. I'm working on the examination of all the files I've done at this period to properly explain what has been done.
The result of this work is the Dash/Plotly application contained in the First_nba_app folder which consist of an interactive page to use features I've learned and get informations 
on players and teams during 20 years of NBA (2001 - 2020).

Close to the deadline, I've had an idea to create a model of Machine Learning to predict the victory of a team by comparing the players (a notebook is also in the folder). 
Because of the lack of time, I've only managed to do it for one year of data, and the first results were actually encouraging with a 67% of good predictions.

Stat data have been scaled per position because it would have no sense to compare the qualities of a Point Guard and a Center. For example, a Point Guard that would make 
medium stats in rebounds and blocks for a Center would have actually good stats for a Point Guard. On the opposite, a Center that is a good passer or good at 3 point shooting
overperform for his position so it's good to take these details in consideration.

But there were some limits to this approach. To make the confront, I've used the mean stats of the year for each player, assuming that players with the most minutes played are always
the starters. I've sorted them by height, assuming that the right confrontation by position should follow the height order (which is partly true in Basketball with
Point Guard < Shooting Guard < Small Forward < Power Forward < Center). Then I've only used the top 10 players per team to make the confront, not knowing who has actually played
which lead to the last issue : this doesn't take account of injury or transfer during the season, it's a generic team of the year that is used for each game.


📊 Data Analysis on PowerBI (EDC Business School)


⚡ Optimized strategy for a cleaner Machine Learning Project




🛠️ Tech Stack

Python 3.10+ Pandas BeautifulSoup Jupyter Notebook Dash/Plotly

📦 Installation

1️⃣ Clone the repository git clone git@github.com:your-username/nba_project.git cd nba_project

2️⃣ Create a virtual environment python -m venv venv source venv/bin/activate # Linux / Mac venv\Scripts\activate # Windows

3️⃣ Install dependencies pip install -r requirements.txt



🧠 Future Improvements

Collecting data to show the strategy I've used in my first project.

👤 Author

Lionel Mockel 📫 Contact: lionel.mockel@gmail.com 🌐 GitHub: @leomockel/cinema_project

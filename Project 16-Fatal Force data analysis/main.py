import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
from flask import Flask, render_template
import json

app= Flask(__name__)

#load data
df = pd.read_csv('Deaths_by_Police_US.csv', encoding='latin-1')
poverty_df = pd.read_csv('Pct_People_Below_Poverty_Level.csv', encoding='latin-1')
poverty_df['poverty_rate'] = pd.to_numeric(poverty_df['poverty_rate'], errors='coerce')
income_df = pd.read_csv('Median_Household_Income_2015.csv', encoding='latin-1')
hs_df = pd.read_csv('Pct_Over_25_Completed_High_School.csv', encoding='latin-1')
race_df = pd.read_csv('Share_of_Race_By_City.csv', encoding='latin-1')
df['race'] = df['race'].fillna('Unknown')
df['armed'] = df['armed'].fillna('Unknown')
df['flee'] = df['flee'].fillna('Unknown')
df['gender'] = df['gender'].fillna('Unknown')


@app.route('/')
def home():
    total_shootings = len(df)
    unarmed = len(df[df['armed'] == 'unarmed'])
    mental_illness = len(df[df['signs_of_mental_illness'] == True])
    body_cam = len(df[df['body_camera'] == True])

    race_counts = df.groupby('race').size().reset_index(name='count')
    race_counts['count'] = race_counts['count'].tolist()

    fig = px.bar(race_counts, x='race', y='count',
                 title='Fatal Shootings by Race',
                 color='race')
    race_chart = fig.to_json()

    return render_template('index.html',
                           total=total_shootings,
                           unarmed=unarmed,
                           mental_illness=mental_illness,
                           body_cam=body_cam,
                           race_chart=race_chart)

@app.route('/race')
def race():

   # shooting by race
    race_counts = df['race'].value_counts().reset_index(name='count')
    race_counts['count'] = race_counts['count'].astype(int)
    race_counts.columns= ['race', 'count']
    fig1= px.bar(race_counts, x='race', y='count',
                 title='Fatal shooting by race',
                 color= 'race')
    race_chart= json.dumps(fig1, cls= plotly.utils.PlotlyJSONEncoder)

    #unarmed by race
    unarmed_df= df[df['armed']=='unarmed']
    unarmed_counts= unarmed_df['race'].value_counts().reset_index(name='count')
    unarmed_counts['count'] = unarmed_counts['count'].astype(int)
    unarmed_counts.columns= ['race','count']
    fig2= px.bar(unarmed_counts, x='race', y='count',
                 title= 'Unarmed Victims by Race',
                 color= 'race')
    unarmed_chart = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('race.html', race_chart= race_chart, unarmed_chart=unarmed_chart)

@app.route('/state')
def state():
   state_counts= df['state'].value_counts().reset_index(name='count')# shooting by state
   state_counts['count'] = state_counts['count'].astype(int)
   state_counts.columns= ['state', 'count']
   fig1= px.bar(state_counts, x= 'state', y='count',
                title='Fatal Shooting by state',
                color='count')
   state_chart = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

   state_poverty= poverty_df.groupby('Geographic Area')['poverty_rate'].mean().reset_index()
   state_poverty.columns= ['state', 'poverty_rate']
   merged= state_counts.merge(state_poverty, on='state')
   fig2= px.scatter(merged, x= 'poverty_rate', y='count',
                    title='Poverty Rate vs Fatal Shooting by State',
                    trendline='ols')

   poverty_chart = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('state.html', state_chart=state_chart, poverty_chart=poverty_chart)


@app.route('/trends')
def trend():
    df['date']= pd.to_datetime(df['date'])
    df['year']= df['date'].dt.year
    year_counts= df['year'].value_counts().sort_index().reset_index(name='count')
    year_counts['count']= year_counts['count'].astype(int)
    year_counts.columns=['year', 'count']
    fig1= px.line(year_counts, x= 'year', y='count',
                  title= 'Fatal Shooting By Year',
                  markers=True)
    year_chart= json.dumps(fig1, cls= plotly.utils.PlotlyJSONEncoder)

    armed_counts= df['armed'].value_counts().head(10).reset_index(name='count')
    armed_counts['count']= armed_counts['count'].astype(int)
    armed_counts.columns=['armed', 'count']
    fig2= px.pie(armed_counts, values= 'count', names='armed',
                 title='Top 10 Weapon Types')
    armed_chart= json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('trends.html',
                         year_chart=year_chart,
                         armed_chart=armed_chart)

@app.route('/demographics')
def demographics():
    fig1= px.histogram(df, x= 'age', title= 'Age Distribution', nbins= 30)
    age_chart= json.dumps(fig1, cls= plotly.utils.PlotlyJSONEncoder)

    gender_counts= df['gender'].value_counts().reset_index(name='count')
    gender_counts['count']=gender_counts['count'].astype(int)
    gender_counts.columns=['gender', 'count']
    fig2= px.pie(gender_counts, values='count', names='gender', title='Gender Breakdown')
    gender_chart= json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)

    flee_counts= df['flee'].value_counts().reset_index(name='count')
    flee_counts['count']=flee_counts['count'].astype(int)
    flee_counts.columns=['flee', 'count']
    fig3= px.pie(flee_counts, values='count', names= 'flee', title= 'Flee Breakdown')
    flee_chart= json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('demographics.html', age_chart=age_chart,gender_chart=gender_chart,
                           flee_chart=flee_chart)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the pre-trained model and data
music = pickle.load(open("df", 'rb'))
similarity = pickle.load(open("model", 'rb'))

def recommend(song, num_recommendations):
    index = music[music['song'] == song].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)
    recommended_music_names = []
    for i in distances[1:num_recommendations + 1]:
        recommended_music_names.append(music.iloc[i[0]].song)
    return recommended_music_names

@app.route('/')
def index():
    music_list = music['song'].values
    return render_template('index.html', music_list=music_list)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    selected_song = request.form['selected_song']
    num_recommendations = int(request.form['num_recommendations'])
    recommended_music_names = recommend(selected_song, num_recommendations)
    return render_template('recommendations.html', recommended_music_names=recommended_music_names)

if __name__ == '__main__':
    app.run(debug=True)

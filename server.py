from flask import Flask, render_template
from database import Database
from tables import Music

app = Flask(__name__)

db=Database()

musicdb=db.music

musicdb.addMusic(Music("Annem","Zeki Müren","Türk Sanat Müziği","1975","Anne Sevgisi","Türkçe","Türkiye"))
musicdb.addMusic(Music("Smooth Criminal","Michael Jackson","Pop","2012","Bad 25th Anniversary","English","U.S.A."))
musicdb.addMusic(Music("Rolling in the Deep","Adele","Rock","2011","21","English","U.K."))
musicdb.addMusic(Music("Maeva in Wonderland","Ibrahim Maalouf","Jazz","2011","Diagnostic","Instrumental","France"))
musicdb.addMusic(Music("Iron","Woodkid","Alternative","2013","Iron","English","France"))
musicdb.addMusic(Music("Beat It","Michael Jackson","Pop","2012","Bad 25th Anniversary","English","U.S.A."))
musicdb.addMusic(Music("The Show Must Go On","Queen","Rock","2011","2011 Remastered","English","U.K."))
musicdb.addMusic(Music("Happy","Pharrell Williams","Pop","2013","Despicable Me 2","English","U.S.A."))
musicdb.addMusic(Music("Coesur Volant","Zaz","Jazz","2011","Single","French","French"))
musicdb.addMusic(Music("Human","Rag'n'Bone Man","Soul","2017","Human (Deluxe)","English","U.S.A."))
musicdb.addMusic(Music("Pump It","Black Eyed Peas","Pop","2005","Monkey Business","English","U.S.A."))
musicdb.addMusic(Music("The Thrill Is Gone","B.B. King","Jazz","1970","Deuces Wild","English","U.S.A."))



@app.route("/")
def index():
    return render_template("index.html",methods=["POST","GET"])

@app.route("/music",methods=["POST","GET"])
def musics():
    getmusics = musicdb.listAllMusic()
    return render_template("musics.html",getmusics=getmusics)


if __name__ == "__main__":
    app.run()

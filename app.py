import os
import requests
import sys
import uuid
import itertools
import operator
from datetime import datetime
from flask import Flask, render_template, json,jsonify,redirect, url_for, session, flash,Markup,request
from flask_bootstrap import Bootstrap,WebCDN
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Required, Length
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from PIL import Image





app = Flask(__name__)


app.config.from_object('config.Config')
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']



db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.extensions['bootstrap']['cdns']['jquery'] = WebCDN('//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/')


# db stuff
class SummonerToAccountID(db.Model):
    __tablename__ = 'sumtoacc'
    name = db.Column(db.String(64), primary_key=True)
    accountid = db.Column(db.Integer, index=True)
    gid = db.Column(db.Integer,  db.ForeignKey('groups.gid'),index=True)


class NameToAvatarFN(db.Model):
    name = db.Column(db.String(64), primary_key=True)
    afn = db.Column(db.String(128))


    def __repr__(self):
        return '%d' % self.name


class APIKey(db.Model):
    __tablename__ = 'apikey'
    id = db.Column(db.Integer,primary_key=True)
    key = db.Column(db.String(100))


class Groups(db.Model):
    __tablename__ = 'groups'
    gid = db.Column(db.Integer, primary_key=True)
    gname = db.Column(db.String(100))
    gdesc = db.Column(db.String(100))
    ati = db.relationship('SummonerToAccountID',backref='index', uselist=False)



class WinList(db.Model):
    __tablename__ = 'winlist'
    accountid = db.Column(db.Integer,index=True)
    gameId = db.Column(db.BigInteger, primary_key=True)
    win = db.Column(db.Boolean)


class MatchData(db.Model):
    __tablename__ = 'matchdata'
    #gametomatch = db.relationship('GameData',backref='gameId')
    accountid = db.Column(db.Integer, index=True)
    lane = db.Column(db.String)
    gameId = db.Column(db.BigInteger, primary_key=True)
    champion = db.Column(db.Integer)
    platformId = db.Column(db.String)
    season = db.Column(db.Integer)
    queue = db.Column(db.Integer)
    role = db.Column(db.String)
    timestamp = db.Column(db.BigInteger)

    def __repr__(self):
        return '%d' % self.id


class GameData(db.Model):
    __tablename__ = 'gamedata'
    accountid = db.Column(db.Integer, index=True)
    gameId = db.Column(db.BigInteger, primary_key=True)
    gameType = db.Column(db.String)
    gameDuration = db.Column(db.BigInteger)
    gameCreation = db.Column(db.BigInteger)
    firstBloodAssist = db.Column(db.Boolean)
    visionScore = db.Column(db.BigInteger)
    magicDamageDealtToChampions = db.Column(db.BigInteger)
    damageDealtToObjectives = db.Column(db.BigInteger)
    totalTimeCrowdControlDealt = db.Column(db.Integer)
    longestTimeSpentLiving = db.Column(db.Integer)
    perk1Var1 = db.Column(db.Integer)
    perk1Var3 = db.Column(db.Integer)
    perk1Var2 = db.Column(db.Integer)
    tripleKills = db.Column(db.Integer)
    perk3Var3 = db.Column(db.Integer)
    nodeNeutralizeAssist = db.Column(db.Integer)
    perk3Var2 = db.Column(db.Integer)
    playerScore9 = db.Column(db.Integer)
    playerScore8 = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    playerScore1 = db.Column(db.Integer)
    playerScore0 = db.Column(db.Integer)
    playerScore3 = db.Column(db.Integer)
    playerScore2 = db.Column(db.Integer)
    playerScore5 = db.Column(db.Integer)
    playerScore4 = db.Column(db.Integer)
    playerScore7 = db.Column(db.Integer)
    playerScore6 = db.Column(db.Integer)
    perk5Var1 = db.Column(db.Integer)
    perk5Var3 = db.Column(db.Integer)
    perk5Var2 = db.Column(db.Integer)
    totalScoreRank = db.Column(db.Integer)
    neutralMinionsKilled = db.Column(db.Integer)
    damageDealtToTurrets = db.Column(db.BigInteger)
    physicalDamageDealtToChampions = db.Column(db.BigInteger)
    nodeCapture = db.Column(db.Integer)
    largestMultiKill = db.Column(db.Integer)
    perk2Var2 = db.Column(db.Integer)
    perk2Var3 = db.Column(db.Integer)
    totalUnitsHealed = db.Column(db.Integer)
    perk2Var1 = db.Column(db.Integer)
    perk4Var1 = db.Column(db.Integer)
    perk4Var2 = db.Column(db.Integer)
    perk4Var3 = db.Column(db.Integer)
    wardsKilled = db.Column(db.Integer)
    largestCriticalStrike = db.Column(db.Integer)
    largestKillingSpree = db.Column(db.Integer)
    quadraKills = db.Column(db.Integer)
    teamObjective = db.Column(db.Integer)
    magicDamageDealt = db.Column(db.BigInteger)
    item2 = db.Column(db.Integer)
    item3 = db.Column(db.Integer)
    item0 = db.Column(db.Integer)
    neutralMinionsKilledTeamJungle = db.Column(db.Integer)
    item6 = db.Column(db.Integer)
    item4 = db.Column(db.Integer)
    item5 = db.Column(db.Integer)
    perk1 = db.Column(db.Integer)
    perk0 = db.Column(db.Integer)
    perk3 = db.Column(db.Integer)
    perk2 = db.Column(db.Integer)
    perk5 = db.Column(db.Integer)
    perk4 = db.Column(db.Integer)
    perk3Var1 = db.Column(db.Integer)
    damageSelfMitigated = db.Column(db.BigInteger)
    magicalDamageTaken = db.Column(db.BigInteger)
    firstInhibitorKill = db.Column(db.Boolean)
    trueDamageTaken = db.Column(db.BigInteger)
    nodeNeutralize = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    combatPlayerScore = db.Column(db.Integer)
    perkPrimaryStyle = db.Column(db.Integer)
    goldSpent = db.Column(db.Integer)
    trueDamageDealt = db.Column(db.BigInteger)
    participantId = db.Column(db.Integer)
    totalDamageTaken = db.Column(db.BigInteger)
    physicalDamageDealt = db.Column(db.BigInteger)
    sightWardsBoughtInGame = db.Column(db.Integer)
    totalDamageDealtToChampions = db.Column(db.BigInteger)
    physicalDamageTaken = db.Column(db.BigInteger)
    totalPlayerScore = db.Column(db.Integer)
    win = db.Column(db.Boolean)
    objectivePlayerScore = db.Column(db.Integer)
    totalDamageDealt = db.Column(db.BigInteger)
    item1 = db.Column(db.Integer)
    neutralMinionsKilledEnemyJungle = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    wardsPlaced = db.Column(db.Integer)
    perkSubStyle = db.Column(db.Integer)
    turretKills = db.Column(db.Integer)
    firstBloodKill = db.Column(db.Boolean)
    trueDamageDealtToChampions = db.Column(db.BigInteger)
    goldEarned = db.Column(db.Integer)
    killingSprees = db.Column(db.Integer)
    unrealKills = db.Column(db.Integer)
    altarsCaptured = db.Column(db.Integer)
    firstTowerAssist = db.Column(db.Boolean)
    firstTowerKill = db.Column(db.Boolean)
    champLevel = db.Column(db.Integer)
    doubleKills = db.Column(db.Integer)
    nodeCaptureAssist = db.Column(db.Integer)
    inhibitorKills = db.Column(db.Integer)
    firstInhibitorAssist = db.Column(db.Boolean)
    perk0Var1 = db.Column(db.Integer)
    perk0Var2 = db.Column(db.Integer)
    perk0Var3 = db.Column(db.Integer)
    visionWardsBoughtInGame = db.Column(db.Integer)
    altarsNeutralized = db.Column(db.Integer)
    pentaKills = db.Column(db.Integer)
    totalHeal = db.Column(db.BigInteger)
    totalMinionsKilled = db.Column(db.Integer)
    timeCCingOthers = db.Column(db.BigInteger)
    



# riot stuff
def GetSummonerInfo(accountName):

    riotapi = APIKey.query.first().key

    r = requests.get('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + accountName, headers={
        "X-Riot-Token": "{}".format(riotapi),
    })

    status_dict = {
        400: 'Bad request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Data not found',
        405: 'Method not allowed',
        415: 'Unsupported media type',
        429: 'Rate limit exceeded',
        500: 'Internal server error',
        502: 'Bad gateway',
        503: 'Service unavailable',
        504: 'Gateway timeout', }

    if r.status_code in status_dict:
        return r.status_code, status_dict[r.status_code]
    return (r.status_code,r.json().get('name'), r.json().get('accountId'))


def choice_query():
    return Groups.query


def sumacc_query():
    return SummonerToAccountID.query


def GetRecentMatches(accountID):
    
    riotapi = APIKey.query.first().key

    r = requests.get('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(accountID), headers={
        "X-Riot-Token": "{}".format(riotapi),
    })

    status_dict = {
        400: 'Bad request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Data not found',
        405: 'Method not allowed',
        415: 'Unsupported media type',
        422: 'Player exists, but hasn\'t played since match history collection began',
        429: 'Rate limit exceeded',
        500: 'Internal server error',
        502: 'Bad gateway',
        503: 'Service unavailable',
        504: 'Gateway timeout', }

    if r.status_code in status_dict:
        return r.status_code, status_dict[r.status_code]
    return r.status_code, r.json().get('matches')


def getGameData(playerID, gameID):
    
    riotapi = APIKey.query.first().key

    r = requests.get('https://na1.api.riotgames.com/lol/match/v3/matches/' + str(gameID), headers={
        "X-Riot-Token": "{}".format(riotapi),
    })

    status_dict = {
        400: 'Bad request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Data not found',
        405: 'Method not allowed',
        415: 'Unsupported media type',
        422: 'Player exists, but hasn\'t played since match history collection began',
        429: 'Rate limit exceeded',
        500: 'Internal server error',
        502: 'Bad gateway',
        503: 'Service unavailable',
        504: 'Gateway timeout', }

    if r.status_code in status_dict:
        return r.status_code, status_dict[r.status_code]

    d = r.json()

    teamdict={}
    for i in r.json().get('teams'):
        teamdict[i['teamId']] = i['win']
    windict={}
    for i in r.json().get('participants'):
        if teamdict[i.get('teamId')] == 'Win':
            windict[i.get('participantId')]='Win'
        else:
            windict[i.get('participantId')]='Lose'
    playerdict={}
    for i in r.json().get('participantIdentities'):
        if windict[i.get('participantId')] == 'Win':
            playerdict[i.get('player').get('accountId')] = 1
        else:  
            playerdict[i.get('player').get('accountId')] = 0

    win = playerdict[playerID]

    for e in d.get('participantIdentities'):
        if e.get('player').get('accountId') == playerID:
            partid = e.get('participantId')
            break
    if partid:
        for lis in r.json().get('participants'):
            if lis.get('participantId') == partid:
                temp = lis.get('stats')
                break
        temp['gameType'] = d.get('gameType')
        temp['gameDuration'] = d.get('gameDuration')
        temp['gameCreation'] = d.get('gameCreation')
        return (temp,win)


def getGameIDs(playerID):
    output = []
    for instance in MatchData.query.filter(MatchData.accountid == playerID):
        output.append(instance.gameId)
    return sorted(output[:20])


# forms
class AddUserForm(FlaskForm):
    name = StringField('LoL name', validators=[DataRequired(), Length(2, 15)])
    gid = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label='gname')
    submit = SubmitField('Submit')

class RemoveUserForm(FlaskForm):
    sname = QuerySelectField(query_factory=sumacc_query, allow_blank=False, get_label='name')
    submit = SubmitField('Submit')

    
    def _repr_(self):
        return '<Choice {}>'.format(self.name)


class SetupGroupForm(FlaskForm):
    gname = StringField('Group name', validators=[DataRequired(), Length(2, 15)])
    gdesc = StringField('Group description (please user fewer than 100 chars)',
                        validators=[DataRequired(), Length(0, 100)])
    submit = SubmitField('Submit')


class MatchDataForm(FlaskForm):
    sname = QuerySelectField(query_factory=sumacc_query, allow_blank=False, get_label='name')
    submit = SubmitField('Submit')

    def _repr_(self):
        return '<Choice {}>'.format(self.name)


class GameDataForm(FlaskForm):
    sname = QuerySelectField(query_factory=sumacc_query, allow_blank=False, get_label='name')
    submit = SubmitField('Submit')

    def _repr_(self):
        return '<Choice {}>'.format(self.name)

class ChartNameForm(FlaskForm):
    sname = QuerySelectField(query_factory=sumacc_query, allow_blank=False, get_label='name')
    submit = SubmitField('Submit')

class APIKeyForm(FlaskForm):
    apikey = StringField('API Key', validators=[DataRequired(), Length(42, 50)])
    submit = SubmitField('Submit')

class RemoveAPIKeyForm(FlaskForm):
    submit = SubmitField('Submit')


# handle 404, 500
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_time=datetime.utcnow()), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', current_time=datetime.utcnow()), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/apikey', methods=['GET','POST'])
def apikey():
    form = APIKeyForm()
    form2 = RemoveAPIKeyForm()
    if form.validate_on_submit():
        apikey = APIKey(id=1,key=form.apikey.data)
        db.session.merge(apikey)
        db.session.commit()

        flash('Successfully added API key', 'success')

        return redirect(url_for('apikey'))
    elif form2.validate_on_submit():
        apikey = APIKey(id=1,key="deleted")
        db.session.merge(apikey)
        db.session.commit()


        return redirect(url_for('apikey'))
    return render_template('apikey.html',form=form,form2=form2,current_time=datetime.utcnow())

@app.route('/setupgroup', methods=['GET', 'POST'])
def setupgroup():
    form = SetupGroupForm()
    if form.validate_on_submit():
        session['gname'] = form.gname.data
        session['gdesc'] = form.gdesc.data

        group = Groups(gname=form.gname.data, gdesc=form.gdesc.data)
        db.session.add(group)
        db.session.commit()

        flash('Success', 'success')

        return redirect(url_for('setupgroup'))
    return render_template('setupgroup.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),
                           platform=session.get('platform'))


@app.route('/matchdata', methods=['GET', 'POST'])
def matchdata():
    form = MatchDataForm()
    if form.validate_on_submit():

        info = GetRecentMatches(form.sname._data.accountid)

        if info[0] != 200:
            flash("{} {}".format(info[0], info[1]), 'danger')
            return redirect(url_for('matchdata'))

        for matches in info[1]:
            exists = MatchData.query.filter(
                MatchData.gameId.ilike("%" + str(matches.get('gameId')) + "%")).first() is not None

            if not exists:
                match = MatchData(accountid=form.sname._data.accountid, lane=matches.get('lane'), gameId=matches.get('gameId'),
                                  champion=matches.get('champion'), platformId=matches.get('platformId'),
                                  season=matches.get('season'), queue=matches.get('queue'), role=matches.get('role'),
                                  timestamp=matches.get('timestamp'))
                db.session.add(match)

        db.session.commit()

        flash('Success', 'success')

        return redirect(url_for('matchdata'))
    return render_template('matchdata.html', form=form, current_time=datetime.utcnow())


@app.route('/adduser', methods=['GET', 'POST'])
def adduser():


    form = AddUserForm()
    form2 = RemoveUserForm()
    if form.validate_on_submit():
        exists = SummonerToAccountID.query.filter(
            SummonerToAccountID.name.ilike("%" + form.name.data + "%")).first() is not None
        if exists:
            flash("User already exists", 'danger')
            return redirect(url_for('adduser'))

        
        info = GetSummonerInfo(form.name.data)

        if info[0] != 200 :
            flash("{} {}".format(info[0], info[1]), 'danger')
            return redirect(url_for('adduser'))

        user = SummonerToAccountID(name=info[1], accountid=info[2], gid=int(form.gid.raw_data[0]))
        db.session.add(user)
        db.session.commit()

        flash('Success', 'success')

        return redirect(url_for('adduser'))
    if form2.validate_on_submit():
        user = SummonerToAccountID.query.filter_by(name=form2.sname.data.name).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('adduser'))



    return render_template('adduser.html', current_time=datetime.utcnow(), form=form, form2=form2,name=session.get('name'),
                           platform=session.get('platform'))


@app.route('/gamedata', methods=['GET', 'POST'])
def gamedata():
    form = GameDataForm()
    if form.validate_on_submit():


        games = getGameIDs(form.sname._data.accountid)
        if not games:
            flash("{}".format("No games found!"), 'danger')
            return redirect(url_for('matchdata'))
        elif len(games) != 20:
            flash("{}".format("Could not find 20 recent games. Can not grab stats."), 'danger')
            return redirect(url_for('matchdata'))

        for game in games:
            exists = GameData.query.filter(
                GameData.gameId.ilike("%" + str(game) + "%")).first() is not None

            if not exists:
                temp = getGameData(form.sname._data.accountid,game)
                gamedata = temp[0]
                win=temp[1]

                if gamedata:
                    gamedata['accountid'] = form.sname._data.accountid
                    gamedata['gameId'] = game

                    if "statPerk0" in gamedata:
                        del gamedata["statPerk0"]
                    if "statPerk1" in gamedata:
                        del gamedata["statPerk1"]
                    if "statPerk2" in gamedata:
                        del gamedata["statPerk2"]

                    gameresult = GameData(**gamedata)
                    db.session.add(gameresult)

                    winner = WinList(accountid=form.sname._data.accountid, gameId=game,win=win)
                    db.session.add(winner)


        db.session.commit()

        flash('Success', 'success')

        return redirect(url_for('gamedata'))
    return render_template('gamedata.html', form=form, current_time=datetime.utcnow())


@app.route("/chart",methods=['GET', 'POST'])
def chart():
    form = ChartNameForm()
    if request.method=="POST":
        if not form.validate_on_submit():
            #flash ('No user specified.','danger')
            return render_template("playerchart.html",form=form,current_time=datetime.utcnow()) 


    if form.validate_on_submit():
        accountid=form.sname._data.accountid
        sname = form.sname.raw_data[0]

        if (GameData.query.filter(GameData.accountid==accountid).count() == 0):
            flash('No games found. Please get game data or find a player who has played recently', 'danger')
            return render_template("playerchart.html",form=form,current_time=datetime.utcnow()) 


        groupinfo = Groups.query.join(SummonerToAccountID).filter(SummonerToAccountID.accountid==accountid).with_entities(Groups.gname,Groups.gdesc).all()

        lanepref=MatchData.query.with_entities(MatchData.lane).filter(MatchData.accountid==accountid).order_by(MatchData.gameId.desc()).limit(20).all()
        lanepref=most_common(lanepref)[0]
        lanepref = interpretlane(lanepref)

        rolepref=MatchData.query.with_entities(MatchData.role).filter(MatchData.accountid==accountid).order_by(MatchData.gameId.desc()).limit(20).all()
        rolepref=most_common(rolepref)[0]
        rolepref=interpretrole(rolepref)


        kills = GameData.query.with_entities(GameData.gameId,GameData.kills).filter(GameData.accountid == accountid).order_by(GameData.gameId.desc()).limit(20).all()
        deaths = GameData.query.with_entities(GameData.gameId,GameData.deaths).filter(GameData.accountid == accountid).order_by(GameData.gameId.desc()).limit(20).all()        
        winquery = WinList.query.with_entities(WinList.win).filter(WinList.accountid==accountid).order_by(WinList.gameId.desc()).limit(20).all()
        wins = winquery.count((True,))
        losses = winquery.count((False,))
        gpm=GameData.query.with_entities(GameData.goldEarned,GameData.gameDuration).filter(GameData.accountid == accountid).order_by(GameData.gameId.desc()).limit(20).all()
        kda=round((GameData.query.with_entities(func.sum(GameData.kills)).filter(GameData.accountid == accountid).scalar()+GameData.query.with_entities(func.sum(GameData.assists)).filter(GameData.accountid == accountid).scalar())/GameData.query.with_entities(func.sum(GameData.deaths)).filter(GameData.accountid == accountid).scalar(),2)
        gpmdata = [round((i/(j/60))) for (i,j) in gpm]
        winpercent = str(round((float(wins)/(wins+losses) * 100),2)) 

        avatarimg = NameToAvatarFN.query.with_entities(NameToAvatarFN.afn).filter(NameToAvatarFN.name==form.sname.raw_data[0]).first()
        if avatarimg:
            avatarimg=avatarimg[0]

        killsvalues = [j for (i,j) in kills]
        deathsvalues = [j for (i,j) in deaths]
        labels = [(x+1) for x in range(0,20)]
        return render_template('chart.html', labels=labels,form=form,sname=sname,groupinfo=groupinfo,lanepref=lanepref,rolepref=rolepref,avatarimg=avatarimg,killsvalues=killsvalues,deathsvalues=deathsvalues, kda=kda,gpmdata=gpmdata,wins=wins,losses=losses,winpercent=winpercent,current_time=datetime.utcnow())
    elif request.method == 'GET':
        return render_template("playerchart.html",form=form,current_time=datetime.utcnow()) 
    #return render_template('chart.html', values=values, form=form,labels=labels, kda=kda,gpmdata=gpmdata,wins=wins,losses=losses,winpercent=winpercent,legend=legend,current_time=datetime.utcnow())

def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

def interpretrole(input):
    dic={}
    dic['DUO_CARRY'] = "Duo carry role"
    dic['SOLO'] = "Solo role"
    dic['NONE'] = "Flex role"
    dic['DUO_SUPPORT'] = "Support role"
    dic['DUO'] = 'Flex role'
    return dic[input]

def interpretlane(input):
    dic={}
    dic['BOTTOM'] = "Bottom lane"
    dic['TOP'] = "Top lane"
    dic['JUNGLE'] = "Jungle lane"
    dic['MID'] = "Mid lane"
    dic['NONE'] = "Flex lane"
    return dic[input]





@app.route("/imageupload",methods=['GET','POST'])
def imageupload():
    return render_template('imageupload.html',current_time=datetime.utcnow())

def _handleUpload(files):
    size = (80,80)
    if not files:
       return None
    filenames = []
    saved_files_urls = []

    file = files['files[]']

    if file and allowed_file(os.path.splitext(file.filename)[1]):
        extension = os.path.splitext(file.filename)[1]
        filename = str(uuid.uuid4()) + extension

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        filenames.append("%s" % (filepath))
        im = Image.open(filepath)
        im.thumbnail(size)
        im.save("./static/thumbnail/" + filename)

    return (filenames,filename)

def allowed_file(String):
    return True


@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        # we are expected to return a list of dicts with infos about the already available files:
        file_infos = []
        imageurls = os.listdir("./static/uploads")
        for file_name in imageurls:
            #file_url = url_for('download', file_name=file_name)
            file_url = "{}{}".format("./static/uploads/",file_name)
            thumbnail_url = "{}{}".format("./static/thumbnail/",file_name)
            file_size = os.path.getsize("{}{}".format("./static/uploads/",file_name))
            file_infos.append(dict(name=file_name,
                                   size=file_size,
                                   url=file_url,
                                   thumbnailUrl=thumbnail_url,
                                   deleteType="DELETE",
                                   deleteUrl="/delete/" + file_name))
        return jsonify(files=file_infos)

    if request.method == 'POST':
        try:
            files = request.files
            file_infos = []
            uploaded_files,file_name = _handleUpload(files)
            file_url = uploaded_files
            thumbnail_url = "{}{}".format("./static/thumbnail/",file_name)
            file_size = os.path.getsize(uploaded_files[0])
            file_infos.append(dict(name=file_name,
                        size=file_size,
                        url=file_url,
                        thumbnailUrl=thumbnail_url,
                        deleteType="DELETE",
                        deleteUrl="/delete/" + file_name))
            return jsonify(files=file_infos)
        except:
            raise
            return jsonify({'status': 'error'})
    
    return redirect(url_for('imageupload'))


@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)
            
            return jsonify({filename: 'True'})
        except:
            return jsonify({filename: 'False'})



@app.route("/chooseavatar",methods=['GET','POST'])
def chooseavatar():
    imageurls = os.listdir("./static/uploads")
    namesquery = SummonerToAccountID.query.with_entities(SummonerToAccountID.name).all()
    names = [i for (i,) in namesquery]



    return render_template('chooseavatar.html',imageurls=imageurls,names=names,current_time=datetime.utcnow())

@app.route("/setavatar",methods=['POST'])
def setavatar():
    if request.method=='POST':
        d = request.get_json()
        addition = indextofilename(d['index'])
        query = NameToAvatarFN(name=d['name'],afn=addition)
        db.session.merge(query)
        db.session.commit()
        return redirect(url_for('chooseavatar'))


def indextofilename(x):
    imageurls = os.listdir("./static/uploads")
    return imageurls[x]


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

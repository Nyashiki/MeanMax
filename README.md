CodinGame contest "mean-max" 2017/11/18 02:00~ (JST)

# ルール
- 円形マップ
- 3人プレイ
- 一人当たり3つの操作ユニット
    - Reaper
    - Destroyer
    - Doof
- プレイヤーの行動は同時
- DestroyerがTankerに衝突することで、Reaperが水を得ることができる。

# マップ
- 半径6000の円形マップ
- Water Townは中心(0, 0)で半径3000

# Looters
- Tanker
    - 発生時では水の量は1
    - マップ外から発生
    - Water Townに向かって動く
    - 1ターンごとに水を1得る
    - 水の量が最大になったら、去る
    - Destroyerによって破壊された場合、今Tankerが持っているのと同じ量だけの水を持つWreckが生成される
    
- Reaper
    - Wreckから1ターン1の水を得る
    - スキルTarを使用することで
        - massを10増加
        - Tankerを破壊不可能に
    - 水を得るためには、turn終了時にReaperの中心がWreck内になければならない
    - 複数のWreckにまたがっているとき、それぞれから1ずつ水をもらう
    - 複数のReaperが同じWreckにいるとき、すべてのReaperが水の量1を得る（これはWreckの水の量が残り1でもである）
- Destroyer
    - Tankerに衝突することでTankerを破壊可能
    - スキルGranadeを使用することで
        - 半径1000以内のLooterをTHROTTLE1000で押すことが可能
        - Destroyer自身にも影響がある
        - vehicleの真ん中に投擲した場合には、対象のvehicleは影響を受けない
    
- Doof
    - 速度に応じてrageを生成する
        - sqrt(vx^2 + vy^2) / 100
        - rageは300以上溜められない
    - スキル Oilを使用することで
        - 摩擦をなくす
        - ReaperがWreckから水を得るのを妨害
    

# 出力
- X Y THROTTLE
    - (X, Y)に向かって加速
- SKILL X Y
    - (X, Y)にスキルを使用
- WAIT
    - 何もしない

# ゲームの終了条件
- 誰か一人が水50を得る
- 200ターン経過

# Expert Rules
- Looterの半径はすべて400
- それぞれにmassが定められており、THROTTLE / mass加速する
- turnの終わりに摩擦が適用される
    - v = v * (1 - 摩擦)
    - 座標、速度は丸め込まれる

- Reaper   : mass=0.5, friction=0.2
- Destroyer: mass=1.5, friction=0.3
- Doof     : mass=1,   friction=0.25
- Tanker   : mass=2.5+0.5*water friction=0.4 THROTTLE=500

# ゲーム進行
- プレイヤーの出力の処理
- スキルの処理
- Tar pool内のVehicleたちのmassを10増やす
- Nitro Grenadeの影響下にあるVehicleたちを、爆発の中心から1000で押す
- Tankerに加速を適用
- プレイヤーが要求した加速をLooterに適用
- turn終了までvehicleたちを移動し、衝突判定をする
- 去っていったTankerを除く
- 新たなTankerを発生させる
- Oil pool内にいないReaperがWreckから水を得る
- 空になったWreckを除く
- Oil pool外のvehicleたちに摩擦の適用
- 座標、速度の丸め込み
- Doofによるrageの生成
- vehicleのmassを変更(これはTar poolによる)
- スキルエフェクトを除く

# スキルについて
- どのスキルも適用範囲は2000で半径は1000
- Tar, Oilは3ターン持続
- Grenadeは1ターンのみ
- rageがないのにスキルを使用すると代わりにWAITになる

- Reaperの使用スキル Tar
    - rage 30
    - massの増加
    - Tankerを破壊できなくする

- Destroyerの使用スキル Granades
    - rage 60

- Doofの使用スキル Oil
    - rage 30
    - Wreckから水を取れなくする
    - 摩擦無効化

#include <iostream>
#include <cassert>
#include <cmath>
#include <sys/time.h>

using namespace std;

// #define DEBUG 

double GetMS() { struct timeval t; gettimeofday(&t, NULL); return (double)t.tv_sec * 1000 + (double)t.tv_usec / 1000; }
double Sigmoid(double x) { return 1.0 / (1.0 + exp(-x)); }

const int INF = 99999;

struct Point {
  int x, y;
  Point() = default;
  Point(int x, int y): x(x), y(y) { }
};

struct Unit : Point {
  double mass;
  int radius;

  Unit() = default;
  Unit(double mass, int radius, int x, int y): 
    mass(mass), radius(radius), Point(x, y) { }
};

struct Reaper : Unit {
  int vx, vy;

  Reaper() = default;
  Reaper(double mass, int radius, int x, int y, int vx, int vy) 
    : Unit(mass, radius, x, y), vx(vx), vy(vy) { }
};

struct Destroyer : Unit {
  int vx, vy;

  Destroyer() = default;
  Destroyer(double mass, int radius, int x, int y, int vx, int vy) 
    : Unit(mass, radius, x, y), vx(vx), vy(vy) { }
};

struct Doof : Unit {
  int vx, vy;

  Doof() = default;
  Doof(double mass, int radius, int x, int y, int vx, int vy) 
    : Unit(mass, radius, x, y), vx(vx), vy(vy) { }
};

struct Tanker : Unit {
  int vx, vy;
  int water;
  int water_capacity;

  Tanker() = default;
  Tanker(double mass, int radius, int x, int y, int vx, int vy, int water, int water_capacity) 
    : Unit(mass, radius, x, y), vx(vx), vy(vy), water(water), water_capacity(water_capacity) { }
};

struct Wreck : Unit {
  int water;

  Wreck() = default;
  Wreck(double mass, int radius, int x, int y, int water) 
    : Unit(mass, radius, x, y), water(water) { }
};

struct Tar : Unit {
  int remain;
  Tar() = default;
  Tar(int radius, int x, int y, int remain): Unit(-1, radius, x, y), remain(remain) {  }
};

struct Oil : Unit {
  int remain;
  Oil() = default;
  Oil(int radius, int x, int y, int remain): Unit(-1, radius, x, y), remain(remain) { } 
};

struct State {
  int rage[3];

  Reaper reaper[3];
  Destroyer destroyer[3];
  Doof doof[3];
  Tanker tanker[32];
  Wreck wreck[32];
  Tar tar[32];
  Oil oil[32];

  int tanker_count, wreck_count, tar_count, oil_count;
  State() = default;
};


int score[3];
State current_state;

void Input(State& s) {
  for (int i = 0; i < 3; i++) {
    cin >> score[i];
#ifdef DEBUG
    cerr << score[i] << " \n"[i == 2];
#endif
  }

  for (int i = 0; i < 3; i++) {
    cin >> s.rage[i];
#ifdef DEBUG
    cerr << s.rage[i] << " \n"[i == 2];
#endif
  }

  int unit_count;
  cin >> unit_count;
#ifdef DEBUG
  cerr << unit_count << endl;
#endif
  s.tanker_count = 0;
  s.wreck_count = 0;
  s.tar_count = 0;
  s.oil_count = 0;
  while (unit_count--) {
    int unit_id, unit_type, player_id, radius, x, y, vx, vy, extra, extra2;
    double mass;
    cin >> unit_id >> unit_type >> player_id >> mass >> radius >> x >> y >> vx >> vy >> extra >> extra2;
#ifdef DEBUG
    cerr << unit_id << " " << unit_type << " " << player_id << " " 
         << mass << " " << radius << " " << x << " " << y << " "
         << vx << " " << vy << " " << extra << " " << extra2 << endl;
#endif
    if (unit_type == 0) { // Reaper
      s.reaper[player_id] = Reaper(mass, radius, x, y, vx, vy);
    } else if (unit_type == 1) { // Destroyer 
      s.destroyer[player_id] = Destroyer(mass, radius, x, y, vx, vy);
    } else if (unit_type == 2) { // Doof
      s.doof[player_id] = Doof(mass, radius, x, y, vx, vy);
    } else if (unit_type == 3) { // Tanker
      s.tanker[s.tanker_count++] = Tanker(mass, radius, x, y, vx, vy, extra, extra2);
    } else if (unit_type == 4) { // Wreck
      s.wreck[s.wreck_count++] = Wreck(mass, radius, x, y, extra);
    } else if (unit_type == 5) { // Tar pool
      s.tar[s.tar_count++] = Tar(radius, x, y, extra);
    } else if (unit_type == 6) { // Oil pool
      s.oil[s.oil_count++] = Oil(radius, x, y, extra);
    } else {
      assert(false);
    }

  }
}

namespace Think {

enum ActionType {
  MOVE, SKILL
};

struct Action {
  ActionType action_type;
  int x, y, throttle;

  Action() = default;
  Action(int x, int y, int throttle): action_type(MOVE), x(x), y(y), throttle(throttle) { }
  Action(int x, int y): action_type(SKILL), x(x), y(y) { }
};

struct Search {
  double score;
  int prev_dir;
  State state;
  Action first_action;

  Search() = default;
  Search(int score, int dir, State state): score(score), prev_dir(dir), state(state) { }
};

class PriorityQueue {

private:

  const int _MAX = 2048;
  Search* _c;
  int _size;

public:

  PriorityQueue() {
    _c = new Search[_MAX + 1];
  }

  ~PriorityQueue() {
    delete[] _c;
  }

  void init() {
    _size = 0;
  }

  bool empty() {
    return _size == 0;
  }

  Search top() {
    return _c[0];
  }

  void push(Search x) {
    int i = _size++;
    if (_size >= _MAX) {
      _size = _MAX - 1;
    }
    while (i > 0) {
      int p = (i - 1) / 2;
      if (_c[p].score >= x.score) {
        break;
      }
      _c[i] = _c[p];
      i = p;
    }
    _c[i] = x;
  }

  void pop() {
    Search x = _c[--_size];
    int i = 0;
    while (i * 2 + 1 < _size) {
      int a = i * 2 + 1, b = i * 2 + 2;
      if (b < _size && _c[b].score > _c[a].score) {
        a = b;
      }
      if (_c[a].score <= x.score) {
        break;
      }
      _c[i] = _c[a];
      i = a;
    }
    _c[i] = x;
  }
};


int dx[8] = { 0, 1, 0, -1, 1, 1, -1, -1 };
int dy[8] = { -1, 1, 0, 1, -1, 1, 1, -1 };

double Distance2D(Point p1, Point p2) {
  return sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
}

void Reaper(const State& state) {
  const int MAX_TURN = 7;
  PriorityQueue que[MAX_TURN + 1];
  for (int i = 0; i < MAX_TURN + 1; i++) {
    que[i].init();
  }
  que[0].push(Search(0, -1, state));

  int loop = 0;
#ifdef DEBUG
  for (; loop < 600; ) {
#else
  double start_time = GetMS();
  while (GetMS() - start_time < 42) {
#endif
    loop++;
    for (int turn = 0; turn < MAX_TURN; turn++) {
      if (que[turn].empty()) {
        continue;
      }      

      Search s = que[turn].top();
      que[turn].pop();

      // ここで取りうる行動を列挙し、turn + 1のqueへpush
      s.score *= 0.95;

      for (int i = 0; i < s.state.wreck_count; i++) {
        double distance = Distance2D(s.state.reaper[0], s.state.wreck[i]);
        if (distance < s.state.wreck[i].radius) {
          bool oiled = false;
          for (int j = 0; j < s.state.oil_count; j++) {
            double oil_distance = Distance2D(s.state.reaper[0], s.state.oil[j]);
            if (turn < s.state.oil[j].remain && oil_distance < s.state.oil[j].radius) {
              oiled = true;
              break;
            }
          }
          if (!oiled) {
            s.score += (500 - 40 * turn + s.state.wreck[i].water); // 早めにとるようにする。
          }        
        }
      }

      for (int dir = 0; dir < 8; dir++) {
        int nx = s.state.reaper[0].x + dx[dir];
        int ny = s.state.reaper[0].y + dy[dir];
        // 要検討: もしかして、常に300で動き続けていいのでは。
        for (int th = 300; th <= 300; th += 100) {
          double ex_score = 0;
          int temp_x  = s.state.reaper[0].x;
          int temp_y  = s.state.reaper[0].y;
          int temp_vx = s.state.reaper[0].vx;
          int temp_vy = s.state.reaper[0].vy;

          double speed = (dir < 4)? th * 2.0 : (th * 1.414); // th / mass / distance ~= th * 0.714
          
          s.state.reaper[0].vx += (nx - s.state.reaper[0].x) * speed;
          s.state.reaper[0].vy += (ny - s.state.reaper[0].y) * speed;
          // move
          s.state.reaper[0].x += s.state.reaper[0].vx;
          s.state.reaper[0].y += s.state.reaper[0].vy;
          // friction
          s.state.reaper[0].vx *= 0.8;
          s.state.reaper[0].vy *= 0.8;

          // destroyerとの距離が近いほど良い。
          /*for (int i = 0; i < 3; i++) {
            if (Distance2D(s.state.reaper[0], s.state.destroyer[i]) < 1000) {
              ex_score += 3;
              if (i == 0) {
                ex_score += 1;
              }
            }
          }*/
          // tankerとの距離が近いほど良い。
          for (int i = 0; i < s.state.tanker_count; i++) {
            if (Distance2D(s.state.reaper[0], s.state.tanker[i]) < 1500) {
              ex_score += 2;
              break;
            }
          }
          for (int i = 0; i < s.state.wreck_count; i++) {
            ex_score -= Distance2D(s.state.reaper[0], s.state.wreck[i]) / 6000.0;
          }
          // でもぶつかるのはだめ。
          bool collision = false;
          for (int i = 1; i < 3; i++) {
            if (Distance2D(s.state.reaper[0], s.state.reaper[i]) < 
              s.state.reaper[0].radius + s.state.destroyer[i].radius) {
              collision = true;
              break;
            } 
          }
          if (!collision) {
            for (int i = 0; i < 3; i++) {
              if (Distance2D(s.state.reaper[0], s.state.destroyer[i]) < 
                    s.state.reaper[0].radius + s.state.destroyer[i].radius) {
                collision = true;
                break;
              } else if (Distance2D(s.state.reaper[0], s.state.doof[i]) < 
                s.state.reaper[0].radius + s.state.doof[i].radius) {
                collision = true;
                break;
              }
            }
          }
          if (!collision) {
            for (int i = 0; i < s.state.tanker_count; i++) {
              if (Distance2D(s.state.reaper[0], s.state.tanker[i]) < 
                    s.state.reaper[0].radius + s.state.tanker[i].radius) {
                collision = true;
                break;
              }
            }
          }
          if (collision) {
            s.state.reaper[0].x = temp_x;
            s.state.reaper[0].y = temp_y;
            s.state.reaper[0].vx = temp_vx;
            s.state.reaper[0].vy = temp_vy;
            ex_score -= 5;
          }

          if (turn == 0) {
            s.first_action = Action(nx, ny, th);  
          }
          
          s.score += ex_score;
          s.prev_dir = dir;
          que[turn + 1].push(s);

          // Undo
          s.state.reaper[0].x = temp_x;
          s.state.reaper[0].y = temp_y;
          s.state.reaper[0].vx = temp_vx;
          s.state.reaper[0].vy = temp_vy;

          s.score -= ex_score;
        }
      }
    }
  }

  Action first_action = que[MAX_TURN].top().first_action;
  cerr << "[reaper] " << endl;
  cerr << "  loop: " << loop << endl;
  cerr << "  score: " << que[MAX_TURN].top().score << endl;

  if (first_action.action_type == MOVE) {
    cout << first_action.x << " " << first_action.y << " " << first_action.throttle << endl;
  } else {
    cout << "SKILL " << first_action.x << " " << first_action.y << endl;
  }
}

void Destroyer(const State& state) {
  // 自分のreaper付近がわちゃわちゃしていたらGrenade。
  if (state.rage[0] > 90) {
    if (Distance2D(state.reaper[0], state.destroyer[0]) < 2000) {
      int count = 0;
      for (int i = 1; i < 3; i++) {
        if (Distance2D(state.reaper[0], state.destroyer[i]) < 1500) {
          count++;
        }
        if (Distance2D(state.reaper[0], state.doof[i]) < 1500) {
          count++;
        }
      }
      if (count >= 2) {
        cout << "SKILL " << state.reaper[0].x << " " << state.reaper[0].y << endl;
        return;
      }
    }
    // 相手だけwreckにいたらGrenade。
    for (int i = 0; i < state.wreck_count; i++) {
      if (Distance2D(state.destroyer[0], state.wreck[i]) < 2000) {
        if (Distance2D(state.reaper[0], state.wreck[i]) < state.wreck[i].radius) {
          continue;
        }
        for (int j = 1; j < 3; j++) {
          if (Distance2D(state.reaper[j], state.wreck[i]) < state.wreck[i].radius) {
            cout << "SKILL " << state.wreck[i].x << " " << state.wreck[i].y << endl;
            return;
          }
        }
      }
    }
  }
  
  
  if (state.tanker_count == 0) {
    int op_max_score_id = (score[1] > score[2])? 1 : 2;
    cout << state.reaper[op_max_score_id].x << " "
       << state.reaper[op_max_score_id].y << " " << 300 << endl;
  } else {
    int dist_min_tanker_idx = 0;
    double distance_min = INF;

    for (int i = 0; i < state.tanker_count; i++) {
      // reaperからの距離が一番近いtankerを壊しに行く。
      // 実験: destroyerから一番近いtankerにしてみる。
      double distance = Distance2D(state.reaper[0], state.tanker[i]);
      if (distance < distance_min) {
        distance_min = distance;
        dist_min_tanker_idx = i;
      } 
    }

    for (int i = 1; i < 3; i++) {
      double distance = Distance2D(state.reaper[i], state.tanker[dist_min_tanker_idx]);
      if (distance > 2000 && distance < distance_min) {
        cout << "WAIT" << endl;
        return;
      }
    }
    cout << state.tanker[dist_min_tanker_idx].x << " "
         << state.tanker[dist_min_tanker_idx].y << " "
         << 300 << endl;
  }
}

void Doof(const State& state) {
  if (state.rage[0] > 30) {
    // 相手にだけwreckを取られる状況なら、とりあえずOilを撒いておく。
    for (int i = 0; i < state.wreck_count; i++) {
      if (Distance2D(state.doof[0], state.wreck[i]) > 2000) {
        continue;
      }
      // 既にオイルが置いてある場合は無視。
      bool already_oiled = false;
      for (int j = 0; j < state.oil_count; j++) {
        if (Distance2D(state.oil[j], state.wreck[i]) < (state.oil[j].radius + state.wreck[i].radius) / 2) {
          already_oiled = true;
          break;
        }
      }
      if (already_oiled) {
        continue;
      }
      double my_dist = Distance2D(state.reaper[0], state.wreck[i]);
      for (int j = 1; j < 3; j++) {
        double op_dist = Distance2D(state.reaper[j], state.wreck[i]);
        if (my_dist > state.wreck[i].radius && op_dist < state.wreck[i].radius) {
          cout << "SKILL " << state.wreck[i].x << " " << state.wreck[i].y << endl;
          return;
        }
      }
    }
  }

  int op_max_score_id = (score[1] > score[2])? 1 : 2;
  cout << state.reaper[op_max_score_id].x << " "
      << state.reaper[op_max_score_id].y << " " << 300 << endl;
}

}

int main() {

  // メインループ
  while (true) {
    Input(current_state);
    double start_time = GetMS();
    Think::Reaper(current_state);
    Think::Destroyer(current_state);
    Think::Doof(current_state);
    double elapsed = GetMS() - start_time;
    cerr << "elapsed: " << elapsed << endl;
  }

  return 0;
}
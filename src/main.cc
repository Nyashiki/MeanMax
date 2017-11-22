#include <iostream>
#include <cassert>

using namespace std;

#define DEBUG 


struct Unit {
  double mass;
  int radius;
  int x, y;

  Unit() = default;
  Unit(double mass, int radius, int x, int y): 
    mass(mass), radius(radius), x(x), y(y) { }
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


struct State {
  int rage[3];

  Reaper reaper[3];
  Destroyer destroyer[3];
  Doof doof[3];
  Tanker tanker[32];
  Wreck wreck[32];

  int tanker_count, wreck_count;
};




namespace Think {


}


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
      // ToDo
    } else if (unit_type == 6) { // Oil pool
      // ToDo
    } else {
      assert(false);
    }

  }
}

int main() {

  // メインループ
  while (true) {
    Input(current_state);

    cout << "WAIT" << endl;
    cout << "WAIT" << endl;
    cout << "WAIT" << endl;
  }

  return 0;
}
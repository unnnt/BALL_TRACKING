
void arah(int input) {
  if (input < 0) {
    lcd.write(0x7F);
  } else {
    lcd.write(0x7E);
  }
}

void tampil(int new_yaw, double PID, int X, int Y, int jarak, int sisi, int persen) {
  static unsigned long lastSwitchTime = 0;
  static bool displayGroup1 = true;

  if (millis() - lastSwitchTime >= 3000) {
    displayGroup1 = !displayGroup1;
    lastSwitchTime = millis();
  }

  if (displayGroup1) {
    lcd.setCursor(10, 0);
    lcd.print("e="); lcd.print(PID);
  } else {
    lcd.setCursor(0, 0);
    if (sisi == -1) {
      lcd.print("Ki,");
    } else if (sisi == 0) {
      lcd.print("Tg,");
    } else if (sisi == 1) {
      lcd.print("Ka,");
    }
    lcd.print(jarak); lcd.print("cm"); lcd.print(persen); lcd.print("%"); lcd.print("    ");
    lcd.setCursor(12, 0); arah(new_yaw);  lcd.print(abs(new_yaw));  lcd.print("  ");
    lcd.setCursor(0, 1);  lcd.print("X"); arah(X); lcd.print(abs(X)); lcd.print(",Y"); arah(Y); lcd.print(abs(Y)); lcd.print("         ");
  }
}

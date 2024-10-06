#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

// Initialize the LCD with the I2C address (0x27 for RG1602A, configured as 20x4)
LiquidCrystal_I2C lcd(0x27, 20, 4);

// Define the keypad layout
const byte ROWS = 4; // Four rows
const byte COLS = 4; // Four columns

// Define the symbols on the buttons of the keypads
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

// Connect keypad ROW0, ROW1, ROW2, ROW3 to these Arduino pins
byte rowPins[ROWS] = {9, 8, 7, 6}; 

// Connect keypad COL0, COL1, COL2, COL3 to these Arduino pins
byte colPins[COLS] = {5, 4, 3, 2}; 

// Create the Keypad object
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

enum State {
  INPUT_ADMISSION,
  SELECT_OPTION
};

State currentState = INPUT_ADMISSION;
String admissionNumber = "";
const int MAX_ADMISSION_LENGTH = 4;

void setup() {
  // Initialize the LCD
  lcd.init();
  lcd.backlight();

  // Initialize Serial Monitor
  Serial.begin(9600);
  
  // Print the initial message
  lcd.setCursor(0, 0);
  lcd.print("Enter Adm Number:");
}

void loop() {
  char key = keypad.getKey();

  if (key) {
    switch (currentState) {
      case INPUT_ADMISSION:
        if (key == '#') {
          if (admissionNumber.length() == MAX_ADMISSION_LENGTH) {
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Adm Number:");
            lcd.setCursor(0, 1);
            lcd.print(admissionNumber);
            Serial.print("Admission Number: ");
            /*
            if (admissionNumber == "6969"){
              lcd.print("Sex");
            } else {
              lcd.print(admissionNumber);
            }
            */
            Serial.println(admissionNumber);
            delay(2000); // Show the admission number for 2 seconds
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Select an option...");
            currentState = SELECT_OPTION;
            admissionNumber = ""; // Clear the admission number for the next entry
          } else {
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Invalid Length");
            delay(1000); // Show error message for 1 second
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Enter Adm Number:");
          }
        } else if (key >= '0' && key <= '9') {
          if (admissionNumber.length() < MAX_ADMISSION_LENGTH) {
            admissionNumber += key;
            lcd.setCursor(0, 1);
            lcd.print(admissionNumber);
            Serial.println(admissionNumber);
          }
        }
        break;
        
      case SELECT_OPTION:
        if (key) {
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print("Option Selected:");
          lcd.setCursor(0, 1);
          lcd.print(key);
          Serial.print("Option Selected: ");
          Serial.println(key);
          delay(2000); // Show the selected option for 2 seconds
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print("Enter Adm Number:");
          currentState = INPUT_ADMISSION; // Reset to admission number input
        }
        break;
    }
  }
}

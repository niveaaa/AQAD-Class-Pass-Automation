#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SS_PIN 10  // SDA pin
#define RST_PIN 9  // RST pin

MFRC522 rfid(SS_PIN, RST_PIN);  // Create MFRC522 instance
Servo myServo;  // Create a Servo object

// Initialize the LCD with the I2C address 0x27 and dimensions 20x4
LiquidCrystal_I2C lcd(0x27, 20, 4);

void setup() {
  Serial.begin(9600);  // Initialize serial communications
  SPI.begin();  // Initialize SPI bus
  rfid.PCD_Init();  // Initialize MFRC522
  myServo.attach(7);  // Attach the servo to digital pin 7
  myServo.write(30);  // Set the servo to 0 degrees initially

  lcd.init();                      // Initialize the LCD
  lcd.backlight();                // Turn on the backlight
  lcd.setCursor(0, 0);
  lcd.print("Scan a card...");
}

void loop() {
  // Look for new cards
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    // Serial.print("UID tag: ");
    String content = "";
    
    for (byte i = 0; i < rfid.uid.size; i++) {
      content += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");  // Add leading zero if needed
      content += String(rfid.uid.uidByte[i], HEX);  // Convert byte to hex
    }
    
    content.toUpperCase();  // Convert to uppercase for readability
    // Serial.println(content);  // Print the UID once
    
    String name;
    if (content == "B0865A7A") {
      name = "Aarush";
    } else if (content == "B04A5A7A") {
      name = "Jahanvi";
    } else if (content == "FBEEA4D5") {
      name = "Tvisha";
    } else if (content == "496B9AE5") {
      name = "Aarshi";
    } else if (content == "3D67A7E5") {
      name = "Aryan";    
    } else {
      name = "Unknown";  // Handle unknown UID
    }
    
    // Display the name on the LCD
    lcd.clear();               // Clear previous display
    lcd.setCursor(0, 0);      // Set cursor to the top-left corner
    lcd.print("Pass is with:");
    lcd.setCursor(0, 1);      // Move cursor to the next line
    lcd.print(name);          // Print the name
    Serial.println(name);
    //  Serial.println(content);
    
    myServo.write(120);  // Rotate the servo to 90 degrees
    delay(5000);        // Wait for 1 second
    
    // Wait for 1 second

    myServo.write(30);  // Rotate the servo to 90 degrees
    delay(1000);        // Wait for 1 second
    
    rfid.PICC_HaltA();  // Halt PICC
  }
}

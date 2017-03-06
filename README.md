This script sends bloomsky data to Citizen Weather Observer Program (CWOP)

Citizen Weather Observer Program: http://wxqa.com/

# Configuration
* Nothing Fancy. Check out the config.json.example file. 

* You need to register your weather station to CWOP here: http://wxqa.com/SIGN-UP.html

* After registering your weather station, you should get a callsign/name for your station. station.name value is the callsign. 

* station.pass value can be empty (Didn't try that way) but you can get your pass here: http://apps.magicbug.co.uk/passcode/ 

* The latitude and longitude is a PITA :) They have to be in DDMM.MM format. Here is more on that: http://ember2ash.com/lat.htm (I have no plan to convert the regular DD-MM-SS to DDMM.MM format in the code. If you want to contribute, send me a pull request)

# Usage

```python /script/folder/cwop.py --config /path/to/config.json```

If you use only like below, it will expect config.json to be in the same folder as the script:
```python /script/folder/cwop.py```


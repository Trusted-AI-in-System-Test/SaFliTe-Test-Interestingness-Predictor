# SaFliTe
## Installing Dependencies

To install the necessary dependencies for SaFliTe, navigate to the SaFliTe folder and run the following command:

```sh
pip install -r requirements.txt
```

## Run SaFliTe

To run SaFliTe, use the following command:

```sh
python SaFliTe.py --test_cases [path to test_cases file] --current_state [path to current_state file] --def_of_int [path to definition_of_interestingness file]
```
Replace [path to test_cases file], [path to current_state file], and [path to definition_of_interestingness file] with the actual paths to your test cases, current state, and definition of interestingness files, respectively.

## Choose a Different LLM

By default, SaFliTe uses ChatGPT3.5 for analysis. If you want to use the Mistral-7B model, follow these steps:

1. Download the Mistral-7B model from the following URL: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF

2. Create a folder named **local_model** in the SaFliTe directory:
	```sh
	mkdir local_model
	```

3. Place the downloaded model in the **local_model** folder.

4. Run the following command:
	```sh
	python SaFliTe.py --test_cases [path to test_cases file] --current_state [path to current_state file] --def_of_int [path to definition_of_interestingness file] --LLM Mistral-7B
	```

## SaFliTe-Enhanced Fuzzing Tool
To run the SaFliTe-enhanced Fuzzing Tool, refer to the detailed instructions available in the respective Fuzzing Tool folder. 

## Bugs Information Provided to SAFLITE
| ID  |   Current State  |   Definition of Interestingness    | 
| ------ | ---- | ------ | 
| Bug NO.3   |The UAV is currently at an altitude of 20 meters, and the flight mode has switched from MISSION to FLIP.| Policy: If and only if roll is less than 45 degree, throttle is greater or equal to 1,500, altitude is more than 10 meters, and the current flight mode is one of ACRO and ALT\_HOLD, then the flight mode can be changed to FLIP. If a test case has the potential to cause the policy violation or drone crash, then this test case is considered an interesting test case.  
| Bug NO.23 case 1  |  Flight Mode: FLIP  | Policy: Deploying a parachute requires following conditions: (1) the motors must be armed, (2) the vehicle must not be in the FLIP or ACRO flight modes, (3) the barometer must show that the vehicle is not climbing, and (4) the vehicle’s current altitude must be above the CHUTE\_ALT\_MIN parameter value. If a test case has the potential to cause the policy violation or drone crash, then this test case is considered an interesting test case. | 
| Bug NO.23 case 2  | Flight Mode: MISSION; RC 3 1900  |  It is the same as Bug NO.23 case 1.|
| Bug NO.24  | The value of the GPS\_POS1\_Z parameter is 2.474742, causing a significant deviation in the GPS sensor measurements. The flight mode has switched from FLIP to ALT\_HOLD.  | Policy:If the Mode is ALT\_HOLD and the throttle stick is in the middle (i.e., 1,500) the vehicle must maintain the current altitude. If a test case has the potential to cause the policy violation or drone crash, then this test case is considered an interesting test case. |
| Bug NO.25  | Flight Mode: ALT\_HOLD, Throttle: 1500  | It is the same as Bug NO.24|
| Bug NO.133  | Flight Mode: ORBIT. After the test case is executed, the GPS will be turned off. |  Policy:If time exceeds COM\_POS\_FS\_DELAY seconds after GPS loss is detected, the GPS fail-safe must be triggered. If a test case has the potential to cause the policy violation or drone crash, then this test case is considered an interesting test case. |
| Bug NO.134  | Flight Mode: Mission. Flying into another location. After the test case is executed, the GPS will be turned off. |  It is the same as Bug NO.133|
| Bug NO.135 | Flight Mode: Mission. Just took off. After the test case is executed, the GPS will be turned off. |  It is the same as Bug NO.133 |

## The Analysis Results of SAFLITE
| Test Case |   Analysis Result |
| ------ | ---- 
| Flight\_Mode  |INTERPRETATION: The test case represents setting the flight mode to 2. It could potentially violate the policy as it is not one of the approved modes (ACRO or ALT\_HOLD) for the FLIP operation. This could lead to the drone performing a flip maneuver in an unsafe or unexpected state, potentially causing a crash or loss of control. Score: 8 out of 10.
| MAV\_CMD\_DO\_PARACHUTE |  INTERPRETATION: The test case represents a user command to deploy the parachute. This test case is highly interesting as deploying a parachute is a critical safety measure. It could potentially cause a policy violation or a drone crash if the conditions for deploying a parachute are not met, such as the motors not being armed, being in the wrong flight mode, or the vehicle not meeting altitude and climbing conditions. Therefore, any command related to parachute deployment requires careful consideration to ensure the safety and integrity of the UAV. Score: 10 out of 10. | 
| RC3  | INTERPRETATION: The test case represents a user input to the control system, possibly related to the remote control channel 3. This test case is quite interesting because it involves user input that could potentially affect the mode or throttle stick position, which could lead to a policy violation or drone crash. The specific impact would depend on the exact nature of the RC3 command and the current state of the UAV. Score: 7 out of 10.|
| ATC\_RAT\_RLL\_FF  | INTERPRETATION: This test case likely represents a command related to the roll rate feedforward for the aircraft's control system. This test case is moderately interesting because it involves a parameter related to the control system. Changes in the roll rate feedforward could potentially affect the stability and control of the UAV, which may lead to a policy violation or drone crash if not handled properly. However, without specific values or context, it's difficult to determine the exact impact of this command. Score: 5 out of 10.|
| COM\_POS\_FS\_DELAY  | INTERPRETATION: This test case represents the delay time after GPS loss is detected before the GPS fail-safe is triggered. This test case is quite interesting because it directly relates to the policy of triggering GPS fail-safe after a certain delay. If the value assigned to COM\_POS\_FS\_DELAY is too high, it could potentially lead to a policy violation or drone crash if the fail-safe is not triggered in time after GPS loss is detected. Therefore, it is important to carefully analyze and test this parameter to ensure the safety and compliance with the policy. Score: 8 out of 10.|

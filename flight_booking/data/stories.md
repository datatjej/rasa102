<!-- ## time path -->
<!-- * greet -->
<!--   - utter_greet -->
<!--   - utter_wh_person -->

<!-- ## inform -->
<!-- * inform_person{"person":"Vlad Maraev"} -->
<!--   - utter_inform -->
<!--   - utter_yn_correct -->
  
<!-- ## incorrect -->
<!-- * deny -->
<!--   - slot{"person": null} -->
<!--   - utter_wh_person -->


## happy path
* greet
  - utter_greet
* request_booking
    - booking_form
    - form{"name": "booking_form"}
    - form{"name": null}

## return path
  - utter_ask_oneway
* affirm
  - utter_ask_return  

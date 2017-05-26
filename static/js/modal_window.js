console.log("inside js");

// 1. (When this will happen) Add Event Listener
// 2. (Where to get data from) Get data from server using AJAX
// 3. (Where to put the data) In the call back function,
//    loop through the customers in json and add them to <ul> in html


// Step 3:
function addDataToHTML(customers){
  console.log(customers);

  // Clear the ul element
  $('#ulCustomers').html('');

  // Add this :
  // <li> Customer: <br>First: <<first name>> <br>Last: <<last name>></li>
  // to HTML for each customer
  for (var i=0; i<customers.length; i++) {
    var first = customers[i].fname;
    var last = customers[i].lname;

    // Q: What to add?
    // A: '<li> Customer: <br>First: <<first variable>> <br>Last: <<last variable>></li>'
    // "<li> Customer: <br>First: " + first + "<br>" + "Last: "+ last + "</li>"
    $('#ulCustomers').append("<li> Customer: <br>First: " + first + "<br>" + "Last: "+ last + "</li>");
 
  }
}

// Step 2:
function getData(evt){
  evt.preventDefault();
  console.log("Show Ajax has been clicked");
  // Get the data from server using AJAX:
  // $.get("route", call_back_function_name);
  $.get('/all_customers.json', addDataToHTML);
}

// Step 1:
$('#show-ajax').on('click', getData);


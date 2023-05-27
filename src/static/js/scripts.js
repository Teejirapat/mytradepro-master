/*!
* Start Bootstrap - New Age v6.0.6 (https://startbootstrap.com/theme/new-age)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-new-age/blob/master/LICENSE)
*/
//
// Scripts
//

function logOut() {
    liff.logout()
    window.location.reload()
  }
  function logIn() {
    liff.login({ redirectUri: window.location.href })
  }
  async function getUserProfile() {
    const profile = await liff.getProfile()
    const Token = await liff.getIDToken()
    const AccessToken = await liff.getAccessToken()

    $.post( "/register", {
      idtoken: Token,
      AccessToken:AccessToken
    });
    document.getElementById("pictureUrl").style.display = "inline"
    document.getElementById("pictureUrl").src = profile.pictureUrl
    document.getElementById("displayName").innerHTML = profile.displayName
    
  }
  async function checkloggedIn(LoggedIn){
    $.post( "/login", {
      LoggedIn: LoggedIn
    });
  }
  async function main() {
    await liff.init({ liffId: "1661115732-pO1eXrrz" })
      if (liff.isLoggedIn()) {
        await checkloggedIn(true)
        await getUserProfile()
        document.getElementById("btnLogIn").style.display = "none"
        document.getElementById("btnLogOut").style.display = "inline"
        document.getElementById("pictureUrl").style.display = "inline"
      } else {
        await checkloggedIn(false)
        document.getElementById("btnLogIn").style.display = "block"
        document.getElementById("btnLogOut").style.display = "none"
        document.getElementById("pictureUrl").style.display = "none"
      }
  }
main()
window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

//table
$(function() {
  $('#table').bootstrapTable()
})

//check notify card or table
function checktable(that){
  var mode = that.checked;
  if (!mode){
      document.body.removeAttribute("data-notify");
      localStorage.removeItem("notifySwitch");
      document.getElementById("table_notify").style.display = "none"
      document.getElementById("card_notify").style.display = "block"
  }
  else{
      document.body.setAttribute("data-notify", "table");
      localStorage.setItem("notifySwitch", "table");
      document.getElementById("card_notify").style.display = "none"
      document.getElementById("table_notify").style.display = "block"
  }
  console.log(mode)
  }

  $('input[maxlength], textarea').maxlength({
    alwaysShow: true, //if true the threshold will be ignored and the remaining length indication will be always showing up while typing or on focus on the input. Default: false.
   // threshold: 10, //Ignored if alwaysShow is true. This is a number indicating how many chars are left to start displaying the indications. Default: 10
    warningClass: "form-text text-muted mt-1", //it's the class of the element with the indicator. By default is the bootstrap "badge badge-success" but can be changed to anything you'd like.
    limitReachedClass: "form-text text-muted mt-1", //it's the class the element gets when the limit is reached. Default is "badge badge-danger". Replace with text-danger if you want it to be red.
    //separator: ' of ', //represents the separator between the number of typed chars and total number of available chars. Default is "/".
    //preText: 'You have ', //is a string of text that can be outputted in front of the indicator. preText is empty by default.
    //postText: ' chars remaining.', //is a string outputted after the indicator. postText is empty by default.
    //showMaxLength: true, //showMaxLength: if false, will display just the number of typed characters, e.g. will not display the max length. Default: true.
    //showCharsTyped: true, //if false, will display just the remaining length, e.g. will display remaining lenght instead of number of typed characters. Default: true.
    placement: 'bottom-right-inside', //is a string, object, or function, to define where to output the counter. Possible string values are: bottom ( default option ), left, top, right, bottom-right, top-right, top-left, bottom-left and centered-right. Are also available : **bottom-right-inside** (like in Google's material design, **top-right-inside**, **top-left-inside** and **bottom-left-inside**. stom placements can be passed as an object, with keys top, right, bottom, left, and position. These are passed to $.fn.css. A custom function may also be passed. This method is invoked with the {$element} Current Input, the {$element} MaxLength Indicator, and the Current Input's Position {bottom height left right top width}.
    
    //appendToParent: true, // appends the maxlength indicator badge to the parent of the input rather than to the body.
    //message: an alternative way to provide the message text, i.e. 'You have typed %charsTyped% chars, %charsRemaining% of %charsTotal% remaining'. %charsTyped%, %charsRemaining% and %charsTotal% will be replaced by the actual values. This overrides the options separator, preText, postText and showMaxLength. Alternatively you may supply a function that the current text and max length and returns the string to be displayed. For example, function(currentText, maxLength) { return '' + Math.ceil(currentText.length / 160) + ' SMS Message(s)';}
    //utf8: if true the input will count using utf8 bytesize/encoding. For example: the '£' character is counted as two characters.
    //showOnReady: shows the badge as soon as it is added to the page, similar to alwaysShow
    //twoCharLinebreak: count linebreak as 2 characters to match IE/Chrome textarea validation
    //customMaxAttribute: String -- allows a custom attribute to display indicator without triggering native maxlength behaviour. Ignored if value greater than a native maxlength attribute. 'overmax' class gets added when exceeded to allow user to implement form validation.
    //allowOverMax: Will allow the input to be over the customMaxLength. Useful in soft max situations.
  });



function show_tip(){
  if($('#exampleModalCenter').is(":visible")){
    $('#exampleModalCenter').hide();
  }
  else if($('#exampleModalCenter').is(":hidden")){
    $('#exampleModalCenter').show();
  }
}


$(window).click(function() {
  $('#exampleModalCenter').fadeOut();
});

$('#exampleModalCenter').click(function(event){
  event.stopPropagation();
});
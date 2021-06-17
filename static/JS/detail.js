import   './jquery.min.js';


$(document).ready(function () {

console.log("hello world")

var like_flag;
var dislike_flag;

if(localStorage.getItem("like") == 1){
          $('.like-btn').css({"background-color": "#d629801a" , "outline": "none"});
        $('.like-inner-flex-1').css({"background-position": "right",  "filter": "grayscale(0%)"});

        } else {
        $('.like-btn').css({"background-color": "transparent", "outline": "none"});
        $('.like-inner-flex-1').css({"background-position": "right",  "filter": "grayscale(100%)"});

        }


if(localStorage.getItem("dislike") == 1){

  $(".dislike-inner-flex-1").css({"filter":"grayscale(0%)"});
  $(".dislike-btn").css({"outline": "none", "background-color":"rgba(8, 109, 38, 0.199)"});

  }
  else
  {                  
  $(".dislike-inner-flex-1").css({"filter": "grayscale(100%)"});
  $(".dislike-btn").css({"outline": "none", "background-color":"transparent"});
  }



var dict = [];
$("#comment-form").submit(function (e)
{     // preventing from page reload and default actions
      e.preventDefault();
      // serialize the data for sending the form data.
      var serializedData = $("#comment-form").serializeArray();
  //  var serializedData = $(this).serialize();   same as above , this is pointing to that particular DOM element such that, Comment-form
      $("#temp").remove();
    // make POST ajax call
  $.ajax({
      type: 'POST',
      url: cmtURL,
      data: serializedData,
      success: function (response) {
          // on successfull creating object
          // 1. clear the form.
          $("#comment-form").trigger('reset');
          var instance = JSON.parse(response["instance"]);
          var fields = instance[0]["fields"];
          var id = String(JSON.parse(response["id"]));
          var num_of_comments = JSON.parse(response["comments"]);
         // if({{object.number_of_comments}} != numberComment)
          $("div #addComment").prepend(
              `<div class="cmt-grandparent" id="div-${id}" >
                <div class = "card mb-3 comment-style" >
                    <span>
                      <strong class="text-info std-text">${fields["name"]||""}</strong>
                      <small class="text-muted std-text">${fields["comment_date"]||""}</small>
                    </span>
                   
                    <hr>
                    
                    <p class="std-text">${fields["body"]||""}</p>
                </div>
                <div class="cmt-buttons" >
                    <div id = "reply_btn" class="R-btn">
                      
                        <button id = "${id}" class="btn btn-info btn-1" onclick="replyFun(this.id)" style="max-width: 18rem;" type="button">
                          <i class="fas fa-reply" id = "reply_count${id}">  0</i>
                        </button>
                    </div>
                    <div class = "delete-cmt">    
                        <button class ="btn btn-danger btn-1" id = "del-cmt-${id}" onclick = "delCmtBtn(${id})"></button>
                    </div>                          
                    
                </div>
              <div class = "card reply-style" id = "doreply${id}">
                   <div class = "reply-style-inner" id="reply_box${id}"></div></div>
               </div>`
          );
          $("#comNum").html(`<p>${num_of_comments} Comment ${numOfCmt} </p>`).addClass("text-secondary");
      }   })  })


$("#likes-form").submit(function (e)
{  e.preventDefault();
  var serializedData = $(this).serializeArray();
  $.ajax({
      type: 'POST',
      url: likeURL,
      data: serializedData,
      success: function (response) {
        var like_count = JSON.parse(response["like"]);
        like_flag = JSON.parse(response["flag"]);
        
        console.log(like_flag);
      
        if(like_flag == 0){      
        $(".like-inner-flex-1").toggleClass('like-animate');       
      }else
      $(".like-inner-flex-1").toggleClass('like-animate'); 
      

      localStorage.setItem("like", like_flag);



      if(like_flag){
          $('.like-btn').css({"background-color": "#d629801a" , "outline": "none"});
        $('.like-inner-flex-1').css({"background-position": "right",  "filter": "grayscale(0%)"});

        } else {
        $('.like-btn').css({"background-color": "transparent", "outline": "none"});
        $('.like-inner-flex-1').css({"background-position": "right",  "filter": "grayscale(100%)"});

        }

        $("#likes").text(`${like_count}`);
        }})
    })





    $("#dislikes-form").submit(function (e)
    {  e.preventDefault();
      var serializedData = $(this).serializeArray();
      $.ajax({
          type: 'POST',
          url: dislikeURL,
          data: serializedData,
          success: function (response) {

            var dislike_count = JSON.parse(response["dislike"]);
            dislike_flag = JSON.parse(response["flag"]);             
            $("#dislikes").text(`${dislike_count}`);

           if(dislike_flag == 1)
            { 
               $(".dislike-inner-flex-1").toggleClass("animated");
            }

            $(".dislike-inner-flex-1").on('animationend', function(){

                   $(this).removeClass('animated');
            });

            localStorage.setItem("dislike", dislike_flag);

            if(dislike_flag){

                    $(".dislike-inner-flex-1").css({"filter":"grayscale(0%)"});
                    $(".dislike-btn").css({"outline": "none", "background-color":"rgba(8, 109, 38, 0.199)"});

                }
            else
                {                  
                    $(".dislike-inner-flex-1").css({"filter": "grayscale(100%)"});
                    $(".dislike-btn").css({"outline": "none", "background-color":"transparent"});
                }



      } })    })



  function replyFun(replies){

      var reply_form = "#doreply" + replies;
      var div_t = "div #reply_box" + replies;
      var rep = "#reply-form" + replies;
      var cond = "#no_reply" + replies;        

      $.ajax({
        type: 'POST',
        url: replyURL,
        data: {"id": replies},
        dataType: "json",
        headers: {"X-CSRFToken":csrfToken},
        success: function(response) {
          var dt = JSON.parse(response["data"]);
          var count = Object.keys(dt).length;
        if($(div_t).is(':empty')){
          $(div_t).empty();
          $(rep).remove();
          $(cond).remove();
          // $("#no_reply"+replies).remove();
          var req_user = requestUser;
        for(var data in dt)
        {$(div_t).append(
              `<dic class = "card reply-section mt-5 p-0"  id = "reply-${replies}-${dt[data]["id"]}" >
              <div class = "card-body mb-3 reply-inner pl-3 pt-2 ">
                 <span>
                   <strong class="text-info std-text">${dt[data]["name"]}</strong>
                   <small class="text-muted std-text">${dt[data]["date"]}</small>
                 </span>
                
                 <hr>
                
                 <p class = "text-light std-text">${dt[data]["body"]}</p>
                </div>
              </div> `    );
          if( req_user == dt[data]["name"])
          {$("#reply-"+replies+"-"+dt[data]["id"]).append(`
          <div class="delete-rpy" id="re_btn${replies}">
            
         <button class ="btn btn-danger btn-1 " id = "repDelbtn${replies}" onclick = "delReplyBtn(${replies},${dt[data]["id"]})"></button>
           </div>`
          );  } }
          if(count == 0)
          $(div_t).prepend(
          `<p id = "no_reply${replies}"><strong>No replies</strong></p>`
          );

          


          $(reply_form).prepend(
              `    <form method="POST" id = "reply-form${replies}" onsubmit = "event.preventDefault();">
                    {% csrf_token %}
                    <div class="form-group">
                      ${replyForm}
                      <button class="btn btn-info mt-1 btn-1" type="submit" style="max-width: 18rem;"  onclick = "ReplyFunc(${replies})">reply  <i class="fas fa-comments"></i>
                      </button>
                    </div></form>`
              );

              $(reply_form).css({"border-style": "solid"});
              $(reply_form).css({"background-color": "rgba(50, 51, 51, 0.425)"});
        }
          else {
            $(div_t).empty();
            $(rep).remove();
            $(reply_form).css({"border-style": "none"});
            $(reply_form).css({"background-color": "transparent"});
          }
         
        },
        error: function (response) {
        console.log("check some errors");
    }
      })}

function ReplyFunc(id)
{  var serializedData = $("#reply-form"+id).serializeArray();
 serializedData.push({"name" : "replyto" , "value" : parseInt(id)});
$.ajax({
    type: 'POST',
    url: getReplyURL,
    data: serializedData,
    dataType: "json",
    headers: {"X-CSRFToken": csrfToken},
    success: function (response) {

        $("#reply-form"+id).trigger('reset');
        var instance = JSON.parse(response["instance"]);
        var fields = instance[0]["fields"];
        var n_replies = JSON.parse(response["replies"]);
        var id_reply = JSON.parse(response["id"]);
        console.log(fields);
       // if({{object.number_of_comments}} != numberComment)
         var div_t = "div #reply_box" + id;
        $(div_t).prepend(
            `<div class = "card reply-section mt-5 p-0"  id = "reply-${id}-${id_reply}" >
              <div class = "card-body mb-3 reply-inner pl-3 pt-2">
                <span>
                 <strong class="text-info std-text">${fields["name"]||""}</strong>
                 <small class="text-muted std-text">${fields["reply_date"]||""}</small>
               </span>
               
               <hr>
               
               <p class = "text-light std-text" >${fields["body"]||""}</p>
               </div>
               <div class="delete-rpy" id="re_btn${id}">
              <button class ="btn btn-danger btn-1" id = "repDelbtn${id}" onclick = "delReplyBtn(${id},${id_reply})" ></button>
                </div>
             </div>`
        );
        var cond = "#no_reply" + id;
        $(cond).remove();
        $("#reply_count"+id).html(`<i  id = "reply_count${id}">  ${n_replies}</i>`);
        // $("#comNum").html(`<p>${numberComment} Comment{{ object.number_of_comments|pluralize }} </p>`).addClass("text-secondary");
    }   })
   }


function delCmtBtn(btn_ID){
console.log("hey");
$.ajax({
type: 'POST',
url: delCmtURL,
data: {"id" : btn_ID},
dataType: "json",
headers: {"X-CSRFToken":csrfToken},
success : function(response) {
var num_of_comments = JSON.parse(response["num_of_comments"]);
$("#div-"+btn_ID).remove();
$("#comNum").html(`<p>${num_of_comments} Comment${numOfCmt} </p>`).addClass("text-secondary");
// $("#reply_count"+btn_ID).html(`<strong class = "text-secondary" id = "reply_count${btn_ID}">${num_of_comments} Reply{{comment.number_of_reply|pluralize}} </strong>`);
 

}})}


function delReplyBtn(cmt, rep){
console.log("hey",rep);
$.ajax({
type: 'POST',
url: delReplyURL,
data: {"id" : cmt , "id_reply" : rep},
dataType: "json",
headers: {"X-CSRFToken": csrfToken},
success : function(response) {
var num_of_replies= JSON.parse(response["num_of_reply"]);

$("#reply_count"+cmt).html(`<i class="fas fa-reply" id = "reply_count${cmt}">  ${num_of_replies}</i>`);
$("#reply-"+cmt+"-"+rep).remove();
  }})}


    $(".errorlist").addClass("alert alert-danger alert-dismissible fade show");





})
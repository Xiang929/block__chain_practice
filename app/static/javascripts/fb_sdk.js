/**
 * Created by twtrubiks on 2016/11/27.
 */
//window.fbAsyncInit = function() {
//      FB.init({
//        appId      : '360249361169115',
//        cookie     : true,  // enable cookies to allow the server to access
//                            // the session
//        xfbml      : true,  // parse social plugins on this page
//        version    : 'v3.0' // use graph api version 2.8
//      });
//  };
//
//  // Load the SDK asynchronously
//(function(d, s, id) {
//    var js, fjs = d.getElementsByTagName(s)[0];
//    if (d.getElementById(id)) return;
//    js = d.createElement(s); js.id = id;
//    js.src = "http://connect.facebook.net/zh_TW/sdk.js#xfbml=1&version=v2.8&appId=360249361169115";
//    fjs.parentNode.insertBefore(js, fjs);
//  }(document, 'script', 'facebook-jssdk'));


<script>
  window.fbAsyncInit = function() {
    FB.init({
      appId      : '{your-app-id}',
      cookie     : true,
      xfbml      : true,
      version    : '{api-version}'
    });

    FB.AppEvents.logPageView();

  };

  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "https://connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));
</script>
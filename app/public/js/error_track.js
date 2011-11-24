
//error tracker
(function() {

    var server = 'http://localhost:8000/'

    function to_server(err) {
        var s = document.createElement('script');
        s.type='text/javascript';
        s.async=true;
        s.src = server + 'api/v0/error_track?e=' + encodeURI(err);
        (document.getElementsByTagName('head')[0]||document.getElementsByTagName('body')[0]).appendChild(s);
    }

    var old_onerror = window.onerror;
    window.onerror = function(err, file, line) {
        to_server(file + "(" + line + ")$$" + err);
        if(old_onerror) old_onerror();
    }
})();

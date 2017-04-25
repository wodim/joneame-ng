/* https://github.com/oneuijs/You-Dont-Need-jQuery */

jnm = {
    ready: function() {
        console.log("?!!");
        var hamburger_el = document.querySelector('#hamburger');
        hamburger_el.addEventListener('click', jnm.ui.hamburger_click);
        /*$("#hamburger").click(function() {
            if ($("#bar").hasClass("nomobile")) {
                $("#bar").removeClass("nomobile");
            } else {
                $("#bar").addClass("nomobile");
            }
        })*/
    },
    ui: {
        hamburger_click: function(e) {
            var menu_el = document.querySelector('.cover .header .sections');
            menu_el.classList.toggle('nomobile');
        },
    },
};

if (document.readyState === 'complete' || document.readyState !== 'loading') {
    jnm.ready();
} else {
    document.addEventListener('DOMContentLoaded', jnm.ready);
}

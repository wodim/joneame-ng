/* https://github.com/oneuijs/You-Dont-Need-jQuery */

jnm = {
    tpl: {
        link_click: '/go/{0}',
    },
    ready: function() {
    },
    ui: {
        hamburger_click: function() {
            var menu_el = document.querySelector('.cover .header .sections');
            menu_el.classList.toggle('nomobile');
        },
        link_click: function(el, id) {
            el.setAttribute('href', jnm.aux.str_format(jnm.tpl.link_click, id));
        },
    },
    aux: {
        // http://stackoverflow.com/a/4673436
        str_format: function(format) {
            var args = Array.prototype.slice.call(arguments, 1);
                return format.replace(/{(\d+)}/g, function(match, number) {
                    return typeof args[number] != 'undefined' ? args[number] : match;
            });
        },
    },
};

if (document.readyState === 'complete' || document.readyState !== 'loading') {
    jnm.ready();
} else {
    document.addEventListener('DOMContentLoaded', jnm.ready);
}

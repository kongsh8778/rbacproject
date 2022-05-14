(function (jq) {
    jq('.multi-menu .title').click(function () {
        // 操作后面的body
        $(this).next().toggleClass('hide');
        $(this).next().removeClass('hide');
        $(this).parent().siblings().find('.body').addClass('hide');
    })

})(jQuery);
$(function() {
    $('.pop').on('click', function() {
        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
        $('#imagemodal').modal('show');   
    });
    $(".form-group:has(input#id_price)").addClass( "price" );
    $(".form-group:has(input#id_theatre_arrangement)").addClass("theatre-arrangement");
    $(".form-group:has(input#id_banquet_arrangement)").addClass("banquet-arrangement");
    $(".form-group:has(select#id_state)").addClass("state");
    $(".form-group:has(select#id_lga)").addClass("lga");
});

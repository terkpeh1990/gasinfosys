$('#topheader .nav-top a' ).on( 'click', function ()
 {
	$( '#topheader .nav-top' ).find( 'li.active' ).removeClass( 'active' );
	$( this ).parent( 'li' ).addClass( 'active' );
});


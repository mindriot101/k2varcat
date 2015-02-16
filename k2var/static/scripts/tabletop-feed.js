var jqueryNoConflict = jQuery;

// begin main function
jqueryNoConflict(document).ready(function(){

    initializeTabletopObject('https://docs.google.com/spreadsheets/d/11Y0WIAQwOVJi-2mP9oVEzHg1EActd6sNxaYfwZT1SB4/pubhtml?gid=0&single=true');

});

// pull data from google spreadsheet
function initializeTabletopObject(dataSpreadsheet){
    var timer = startProgress();
    Tabletop.init({
        key: dataSpreadsheet,
        callback: function(dataSource) { writeTableWith(dataSource, timer); },
        simpleSheet: true,
        debug: false
    });
}

function startProgress() {
    var $bar = $('#progress-bar');
    return setInterval(function() {
        updateProgress($bar.width() + 40);
    }, 300);
}

function updateProgress(value) {
    var $bar = $('#progress-bar');
    $bar.width(value);
}

// create table headers
function createTableColumns(){

    /* swap out the properties of mDataProp & sTitle to reflect
    the names of columns or keys you want to display.
    Remember, tabletop.js strips out spaces from column titles, which
    is what happens with the More Info column header */

    var tableColumns =   [
		{'mDataProp': 'epicid', 'sTitle': 'EPIC ID', 'sClass': 'center'},
		{'mDataProp': 'type', 'sTitle': 'Type', 'sClass': 'center'},
		{'mDataProp': 'range', 'sTitle': 'Range', 'sClass': 'center'},
		{'mDataProp': 'period', 'sTitle': 'Period', 'sClass': 'center'},
		{'mDataProp': 'amplitude', 'sTitle': 'Amplitude', 'sClass': 'center'},
		{'mDataProp': 'proposal', 'sTitle': 'Proposal Information', 'sClass': 'center'}
	];
    return tableColumns;
}

// create the table container and object
function writeTableWith(dataSource, timer){
    $('#progress-bar').css('width', "100%");
    clearInterval(timer);

    // Add delay to make it look nice
    setTimeout(function() {
        jqueryNoConflict('#demo').html('<table cellpadding="0" cellspacing="0" border="0" class="display table table-bordered table-striped" id="data-table-container"></table>');

        var oTable = jqueryNoConflict('#data-table-container').dataTable({
            'sPaginationType': 'bootstrap',
            'iDisplayLength': 25,
            'aaData': dataSource,
            'aoColumns': createTableColumns(),
            'oLanguage': {
                'sLengthMenu': '_MENU_ records per page'
            }
        });
    }, 200);

};

//define two custom functions (asc and desc) for string sorting
jQuery.fn.dataTableExt.oSort['string-case-asc']  = function(x,y) {
	return ((x < y) ? -1 : ((x > y) ?  0 : 0));
};

jQuery.fn.dataTableExt.oSort['string-case-desc'] = function(x,y) {
	return ((x < y) ?  1 : ((x > y) ? -1 : 0));
};

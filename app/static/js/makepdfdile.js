function showMessage(msg) {
    alert(msg + " 123")
}

function getPDF(obj) {
    // import { pdfMake } from './pdfmake/pdfmake.min'
    obj.pageMargins = [50, 20, 20, 20]
    obj.footer = function (currentPage, pageCount) {
        return {
            text: currentPage.toString(),
            alignment: 'center'
        };
    },
    console.log(obj);
    pdfMake.tableLayouts = {
        noBordersAndPaddings: {
            hLineWidth: function (i) {
                return 0;
            },
            vLineWidth: function (i) {
                return 0;
            },
            paddingLeft: function (i) {
                return 0;//i && 4 || 0;
            },
            paddingRight: function (i, node) {
                return 0; //(i < node.table.widths.length - 1) ? 4 : 0;
            },
            paddingTop: function (i) {
                return 1;
            },
            paddingBottom: function (i) {
                return 1;
            },
        },
        noPaddings: {
            paddingLeft: function (i) {
                return i && 4 || 2;
            },
            paddingRight: function (i, node) {
                return (i < node.table.widths.length - 1) ? 4 : 2;
            },
            paddingTop: function (i) {
                return 1;
            },
            paddingBottom: function (i) {
                return 1;
            },
        },
        headerLine: {
            hLineColor: 'darkblue',
            defaultBorder: false,
            paddingLeft: function (i) {
                return 0;//i && 4 || 2;
            },
            paddingRight: function (i, node) {
                return 0;//(i < node.table.widths.length - 1) ? 4 : 2;
            },
            paddingTop: function (i) {
                return 2;
            },
            paddingBottom: function (i) {
                return 1;
            },
        },
        subHeaderLine: {
            hLineColor: 'black',
            defaultBorder: false,
            paddingLeft: function (i) {
                return 0;//i && 4 || 2;
            },
            paddingRight: function (i, node) {
                return 0;//(i < node.table.widths.length - 1) ? 4 : 2;
            },
            paddingTop: function (i) {
                return 2;
            },
            paddingBottom: function (i) {
                return 2;
            },
        }
    }
    var pdf = pdfMake.createPdf(obj).download();
}
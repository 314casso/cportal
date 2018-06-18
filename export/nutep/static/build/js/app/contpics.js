import {utils} from '../utils.js';

var appContpics = new Vue({
    el: '#app-contpics',
    data: {
        items: [],
        loading: false,
        error: '',
        updated: null
    },
    delimiters: ["<%", "%>"],
    mounted() {			
        if (this.$el) {
            this.fetchData();          
        }
    },
    methods: {
        checkJob: function (job) {
            utils.checkJob(job, this);
        },
        jobSuccess: function () {
            this.fetchData();
        }, 
        pingService: function () {
            this.loading = true;
            var period = $('#period').data('datepicker').getFormattedDate('ddmmyyyy');
            utils.pingData('/api/pingcontpics/' + period + '/', this);
        },       
        fetchData: function () {
            console.log("fetchData");
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/api/contpicsevents/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, utils.reviver);
                    self.items = data;
                    if (self.items) {
                        self.updated = self.items[0].date;
                    }						
                } catch (e) {
                    self.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function (url) {
            window.location.href = url;
        },
        log: function () {
            console.log($('#period').data('datepicker').getFormattedDate('ddmmyyyy'));
        }
    },
    filters: {
        shortdate: function (date) {
            return utils.shortdate(date);
        },
        moment: function (date) {				
            return utils.moment(date);									
        },
        upper: function (date) {
            return utils.upper(date);					
        },
    },
});

$('#period').datepicker({
    format: "MM yyyy",
    language: "ru",
    minViewMode: 1,
    maxViewMode: 2    
}).on('changeDate', function(e){
    $(this).datepicker('hide');
});

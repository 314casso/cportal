import {utils} from '../utils.js';

var appDealStats = new Vue({
    el: '#app-dealstats',
    data: {
        error: '',
        data: {}
    },
    delimiters: ["<%", "%>"],
    mounted() {
        this.fetchData();
    },    
    methods: {
        fetchData: function () {
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/api/dealstats/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, utils.reviver);
                    self.data = data.deal_stats;
                } catch (e) {
                    self.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        }
    },
    filters: {
        shortdate: function (date) {
            return utils.shortdate(date);
        },
        moment: function (date) {				
            return utils.moment(date);									
        },        
    },
});
import {utils} from '../utils.js';

var appTerminalExport = new Vue({
    el: '#app-terminal-export',
    data: {
        items: [],
        loading: false,
        error: '',
        search: '',
        currentItem: null,
        container: null,
    },
    delimiters: ["<%", "%>"],
    mounted() {			
        this.fetchData();
        this.pingData();
    },
    methods: {
        checkJob: function (job) {
            utils.checkJob(job, this);
        },
        jobSuccess: function () {
            this.fetchData();
        },
        pingData: function () {
            this.loading = true;
            utils.pingData('/api/pingterminalexport/', this);
        },
        fetchData: function () {
            console.log("fetchData");
            var xhr = new XMLHttpRequest();            
            xhr.open('GET', '/api/terminalexportevents/');
            xhr.onload = () => {
                try {
                    var data = JSON.parse(xhr.responseText, utils.reviver);
                    this.items = data;	
                    if (data && data[0].terminalexports) {				                        
                        this.currentItem = data[0].terminalexports[0];
                    }					
                } catch (e) {
                    this.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function (url) {
            window.location.href = url;
        },
        clearSearch: function () {
            this.search = "";
        },
        setCurrentItem: function (item) {
            this.currentItem = item;
        },
        setContainer: function (terminalexport) {
            if (!terminalexport.container) {
                return false;
            }
            this.container = terminalexport.container;            
            if (this.container.stuffs) {                
                this.container.total = {
                    'netweight': utils.sum(this.container.stuffs, 'netweight'),
                    'grossweight': utils.sum(this.container.stuffs, 'grossweight'),
                    'quantity': utils.sum(this.container.stuffs, 'quantity')                
                }
            }
            return true;
        },
        rows: function (item) {
            if (item) {
                var rows = item.terminalexports;
                var self = this;
                return rows.filter(function (row) {
                    if (!self.search) {
                        return true;							
                    }												
                    return row.container.number.search(new RegExp(self.search, "i")) != -1; 
                });				
            }				
        },
    },
    filters: {
        shortdate: (date) => {
            return utils.shortdate(date);
        },
        moment: (date) => {				
            return utils.moment(date);									
        },
        upper: (date) => {
            return utils.upper(date);					
        },
        number: (x) => {
            return utils.number(x);					
        },
    },
});
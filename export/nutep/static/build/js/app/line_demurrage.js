import {utils} from '../utils.js';

Vue.component('v-select', VueSelect.VueSelect);

var appTerminalExport = new Vue({
    el: '#app-terminal-export',
    components: {
        vuejsDatepicker,       
    },
    data: {
        items: [],
        loading: false,
        error: '',
        search: '',
        currentItem: null,
        container: null,
        stats: {
            total_rows: 0,
        },
        filter: {
            number: '',
            size: [],
            type: [],
            line: [],
            date: null,
            terminal: [],
            status: [],
            cargomark: [],
            departed: true
        },
        highlighted: {            
            dates: [
              new Date(),              
            ]            
        },
    },
    delimiters: ["<%", "%>"],
    created() {		
        this.pingData();        
    },
    mounted() {			
        this.fetchData();        
    },
    computed: {            
        isFiltered: function () {
            return this.filter.number || this.filter.size.length || this.filter.type.length 
                || this.filter.line.length || this.filter.date || this.filter.terminal.length
                || this.filter.status.length || this.filter.cargomark.length || this.filter.departed;
        },
        filterOptions: function () {
            let result = { 
                sizes: [], 
                lines: [],
                types: [],
                terminals: [],
                statuses: [],
                cargomarks: []
            };
            if (this.items.length == 0) {
                return result; 
            }
            var rows = this.items[0].linedemurrages;            
            let sizes = new Set();
            let types = new Set();
            let lines = new Set();
            let terminals = new Set();
            let statuses = new Set();
            let cargomarks = new Set();
            rows.forEach(function(elem, i, arr) {                                    
                if (elem.container) {
                    sizes.add(elem.container.size);
                    lines.add(elem.container.line);
                    types.add(elem.container.type);
                    terminals.add(elem.container.terminal);
                }
                if (elem.status) {
                    statuses.add(elem.status);    
                }
                if (elem.cargomark) {
                    cargomarks.add(elem.cargomark);    
                }
             });
             result.sizes = Array.from(sizes);
             result.lines = Array.from(lines);
             result.types = Array.from(types);
             result.terminals = Array.from(terminals);
             result.statuses = Array.from(statuses);
             result.cargomarks = Array.from(cargomarks);
             return result;
        }
    },
    methods: {
        customFormatter(date) {
            return moment(date).format('DD.MM.YYYY');
        },        
        checkJob: function (job) {
            utils.checkJob(job, this);
        },
        jobSuccess: function () {
            this.fetchData();
        },
        pingData: function () {
            this.loading = true;
            utils.pingData('/api/pinglinedemurrage/', this);
        },
        fetchData: function () {
            NProgress.start();
            var xhr = new XMLHttpRequest();            
            xhr.open('GET', '/api/linedemurrages/');
            xhr.onload = () => {
                try {                            
                    var data = JSON.parse(xhr.responseText, utils.reviver);                    
                    this.items = data;	
                    if (data && data[0].linedemurrages) {				                        
                        this.currentItem = data[0].linedemurrages[0];                                                            
                    }					
                } catch (e) {
                    this.error = "Произошла ошибка обновления данных: " + e;                                        
                } finally {
                    NProgress.done();
                }
            };
            xhr.send();
        },
        open: function (url) {
            window.location.href = url;
        },
        clearSearch: function () {
            this.filter.number = "";
        },
        clearDate: function () {
            this.filter.date = null;                        
        },
        clearFilter: function () {
            this.filter.number = '';
            this.filter.size = [];
            this.filter.type = [];
            this.filter.line = [];
            this.filter.terminal = [];
            this.filter.date = null;   
            this.filter.status = [];
            this.filter.cargomark = [];
            this.filter.departed = false;
        },
        setCurrentItem: function (item) {
            this.currentItem = item;
        },
        setContainer: function (terminalexport) {
            if (!terminalexport.container) {
                return false;
            }
            this.container = terminalexport.container;                        
            return true;
        },                
        rows: function (item) {
            if (item) {
                var rows = item.linedemurrages;
                var self = this;
                var filtered = rows.filter(function (row) {                    
                    if (!self.isFiltered) {
                        return true;
                    }
                    if (self.filter.number && !(row.container.number.search(new RegExp(self.filter.number, "i")) != -1)) {
                        return false;
                    }						
                    if (self.filter.type.length && !self.filter.type.includes(row.container.type)) {	
                        return false;                       
                    }
                    if (self.filter.size.length && !self.filter.size.includes(row.container.size)) {	
                        return false;                       
                    }
                    if (self.filter.line.length && !self.filter.line.includes(row.container.line)) {	
                        return false;                       
                    }
                    if (self.filter.terminal.length && !self.filter.terminal.includes(row.container.terminal)) {	
                        return false;                       
                    }
                    if (self.filter.status.length && !self.filter.status.includes(row.status)) {	
                        return false;                       
                    }
                    if (self.filter.cargomark.length && !self.filter.cargomark.includes(row.cargomark)) {	
                        return false;                       
                    }
                    if (self.filter.departed && row.container.dateout) {	
                        return false;                       
                    }
                    if (self.filter.date && !(moment(self.filter.date).format('YYYY-MM-DD') == moment(row.emptydate).format('YYYY-MM-DD'))) {	                        
                        return false;                       
                    }
                    return true; 
                });	                
                self.stats.total_rows = filtered.length;                                
                self.stats.total_unfiltered = rows.length;
                return filtered;		
            }				
        },
    },
    filters: {
        shortdate: (date) => {
            return utils.shortdate(date);
        },
        date: (date) => {
            return utils.date(date);
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


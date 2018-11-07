import {utils} from '../utils.js';

Vue.component('v-select', VueSelect.VueSelect);

var appTerminalExport = new Vue({
    el: '#app-terminal-export',    
    data: {
        items: [],
        loading: false,
        error: '',
        search: '',        
        stats: {
            total_rows: 0,
        },
        filter: {
            name: '',
            size: [],
            type: [],
            extension: []            
        },        
        contracts: [],
        contract: null
    },
    delimiters: ["<%", "%>"],
    mounted() {			        
        this.fetchContracts();
        this.pingContracts();         
    },
    computed: {            
        isFiltered: function () {
            return this.filter.name || this.filter.type.length || this.filter.extension.length;
        },
        filterOptions: function () {             
            let result = {                 
                extensions: [],
                types: []                
            };
            if (this.items.length == 0) {
                return result; 
            }            
            
            var rows = this.items[0].contractevent.files;            
            
            if (!rows) {
                return result; 
            }            
            let types = new Set();
            let extensions = new Set();
            
            rows.forEach(function(elem, i, arr) {                                    
                if (elem) {             
                    extensions.add(elem.extension);
                    types.add(elem.doc_type);                    
                }
             });             
             result.extensions = Array.from(extensions);             
             result.types = Array.from(types);             
             result.types.sort();
             return result;
        }
    },
    watch: {
        contract: function (val) {
            if(val) {
                this.pingContractFiles(val);
            } else {
                this.fetchContractFiles();                
            }
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
            this.fetchContracts(); 
            this.fetchContractFiles();
            console.log(this.filterOptions);
        },
        pingContracts: function () {
            this.loading = true;
            utils.pingData('/pingcontracts/', this);
        },
        pingContractFiles: function (contract) {
            this.loading = true;
            utils.pingData('/pingcontractfiles/' + contract.id + '/', this);
        },
        fetchContractFiles: function () {            
            if (!this.contract) {
                this.items = []
                this.stats.total_rows = 0;                                
                this.stats.total_unfiltered = 0;    
                return;
            }
            var xhr = new XMLHttpRequest();            
            xhr.open('GET', '/api/contractfiles/?contract=' + this.contract.id);
            xhr.onload = () => {
                try {
                    var data = JSON.parse(xhr.responseText, utils.reviver);
                    this.items = data;	                    
                } catch (e) {
                    this.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        fetchContracts: function () {            
            var xhr = new XMLHttpRequest();            
            xhr.open('GET', '/api/contracts/');
            xhr.onload = () => {
                try {
                    var data = JSON.parse(xhr.responseText, utils.reviver);
                    this.contracts = data;	                    
                } catch (e) {
                    this.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function (file) {
                var wnd = window.open('about:blank', '_blank');
                var xhr = new XMLHttpRequest();
                var self = this;
                xhr.open('GET', '/getfileurl/' + file.guid + '/');
                xhr.onload = function () {
                        try {
                                var data = JSON.parse(xhr.responseText);
                                if (data.url) {
                                        wnd.location = data.url;
                                }
                    } catch (e) {
                        appSettings.error = "Произошла ошибка обновления данных: " + e + ": " + xhr.responseText;
                    }
                }
                xhr.send();
        },        
        clearSearch: function () {
            this.filter.name = "";
        },
        clearDate: function () {
            this.filter.date = null;            
            console.log('OK');
        },
        clearFilter: function () {
            this.filter.name = '';
            this.filter.size = [];
            this.filter.type = [];
            this.filter.extention = [];            
        },        
        setContainer: function (terminalexport) {
            if (!terminalexport.container) {
                return false;
            }
            this.container = terminalexport.container;                        
            return true;
        },                
        rows: function (item) {
            if (item && item.contractevent && item.contractevent.files) {                   
                var rows = item.contractevent.files.slice();

                rows.sort(function (a, b) {
                    if (a.doc_type > b.doc_type) {
                      return 1;
                    }
                    if (a.doc_type < b.doc_type) {
                      return -1;
                    }                    
                    return 0;
                  });

                var self = this;
                var filtered = rows.filter(function (row) {                    
                    if (!self.isFiltered) {
                        return true;
                    }
                    if (self.filter.name && !(row.title.search(new RegExp(self.filter.name, "i")) != -1)) {
                        return false;
                    }						
                    if (self.filter.type.length && !self.filter.type.includes(row.doc_type)) {	
                        return false;                       
                    }                    
                    if (self.filter.extension.length && !self.filter.extension.includes(row.extension)) {	
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
        humanFileSize: (size) => {            
            return utils.humanFileSize(size);
        },
    },
});


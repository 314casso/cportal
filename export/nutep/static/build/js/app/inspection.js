function getHhmm(value) {
	if (value == 0) return moment.utc(0).format('HH:mm');
	var duration = moment.duration(value * 1000);
	return duration.format("hh:mm", { trim: false });
}

var app = new Vue({
    el: '#inspection', 
    delimiters: ["<%", "%>"],   
	data: {	 		 
        curdoc: null,      
		info: null,		
        errors: [],
        loading: false,
        error: '',
        data: [],        
		index: null,
		inspection: {}
	},
	created: function () {		        
		this.loadData();		
	},
	computed: {	
        sortedDate(){            
            return this.data.sort((a, b) => new Date(b.date) - new Date(a.date));
		},
		inspectionImages() {			
			if (this.inspection.files) {
				return this.inspection.files.filter(image => image.extension != 'pdf');
			}
			return []
		},
		inspectionDocs() {
			if (this.inspection.files) {			
				return this.inspection.files.filter(image => image.extension == 'pdf');
			}
			return []
		}
	},	
	methods: {		
		loadData: function () {
			this.errors = [];			
			this.loading = true;
			fetch('/inspections/')
				.then(res => {
					this.updated = new Date();
					this.status = res.status;
					if (res.status !== 200) {  
						err = {}
						err.message = getShortDate(this.updated) + '. Ошибка загрузки данных. Ответ сервера: ' + res.status;
						this.errors.push(err);
						this.loading = false;
						return;  
					};

					res.json().then(json => {
                        this.data = JSON.parse(json);						                        
                        this.loading = false;
					});
				});
		},				
		loadItem: function (guid) {
			this.errors = [];
			this.loading = true;			
			fetch('/api/inspection/' + guid + '/?format=json')
				.then(res => {					
					if (res.status !== 200) {  
						err = {}
						err.message = getShortDate(this.updated) + '. Ошибка загрузки данных. Ответ сервера: ' + res.status;
						this.errors.push(err);
						this.loading = false;
						return;  
					};

					res.json().then(json => {
                        this.inspection = json;						                        
                        this.loading = false;
					});
				});
		},
		resetItem: function (guid) {
			this.errors = [];
			this.loading = true;			
			fetch('/getinspection/' + guid + '/')
				.then(res => {					
					if (res.status !== 200) {  
						err = {}
						err.message = getShortDate(this.updated) + '. Ошибка загрузки данных. Ответ сервера: ' + res.status;
						this.errors.push(err);
						this.loading = false;
						return;  
					};

					res.json().then(json => {
                        this.loadItem(guid);
                        this.loading = false;
					});
				});
		},
        containerClick:  function (curdoc) {
			this.curdoc = curdoc;
			this.loadItem(curdoc.guid);
            // $('.collapse').collapse('toggle');            
        }
	},	
	filters: {
		hhmm: function (value) {
			return getHhmm(value);
		},
		shortdate: function shortdate(date) {
			return getShortDate(date);
		},
		humanFileSize: function(bytes){
			return humanFileSize(bytes, true);
		}
	}
})

function getShortDate(date){
	if (date) {
		return moment(date).format('DD.MM.YYYY');
	}
}

function humanFileSize(bytes, si) {
    var thresh = si ? 1000 : 1024;
    if(Math.abs(bytes) < thresh) {
        return bytes + ' B';
    }
    var units = si
        ? ['kB','MB','GB','TB','PB','EB','ZB','YB']
        : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while(Math.abs(bytes) >= thresh && u < units.length - 1);
    return bytes.toFixed(1)+' '+units[u];
}


$(document).on('click', '[data-toggle="lightbox"]', function(event) {
    event.preventDefault();
    $(this).ekkoLightbox();
});
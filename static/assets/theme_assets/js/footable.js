$(function() {
    $('.adv-table').footable({
      filtering: {
        enabled: true
      },
      "paging": {
              "enabled": true,
			  "current": 1
	  },
      strings: {
        enabled: false
      },
      "filtering": {
              "enabled": true
          },
      components: {
          filtering: FooTable.MyFiltering
      },
    }); 
  });
  
FooTable.MyFiltering = FooTable.Filtering.extend({
	construct: function(instance){
		this._super(instance);
		// props for the first dropdown
		this.statuses = ['Web Developer','Senior Manager','UX/UI Desogner','Content Writer','Graphic Designer','Marketer','Project Manager','UI Designer','Business Development'];
		this.statusDefault = 'Davomiyligi';
		this.$status = null;
		// props for the second dropdown
		this.jobTitles = ['Active','deactivate','Blocked'];
		this.jobTitleDefault = 'Status';
		this.$jobTitle = null;
	},
	$create: function(){
		this._super();
		var self = this;
		// create the status form group and dropdown
		var $status_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position my-md-10 my-10 mr-sm-20 mr-0 '})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);

		self.$status = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onStatusDropdownChanged)
			.append($('<option/>', {text: self.statusDefault}))
			.appendTo($status_form_grp);

		$.each(self.statuses, function(i, status){
			self.$status.append($('<option/>').text(status));
		});



		// create the job title form group and dropdown
		var $job_title_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__status my-md-10 mt-10 mb-0 mr-sm-30 mr-0'})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);

		self.$jobTitle = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onJobTitleDropdownChanged)
			.append($('<option/>', {text: self.jobTitleDefault}))
			.appendTo($job_title_form_grp);

		$.each(self.jobTitles, function(i, jobTitle){
			self.$jobTitle.append($('<option/>').text(jobTitle));
		});
	},
	_onStatusDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.statusDefault){
			self.addFilter('position', selected, ['position']);
		} else {
			self.removeFilter('position');
		}
		self.filter();
	},
	_onJobTitleDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.jobTitleDefault){
			self.addFilter('status', selected, ['status']);
		} else {
			self.removeFilter('status');
		}
		self.filter();
	},
	draw: function(){
		this._super();
		// handle the status filter if one is supplied
		var status = this.find('position');
		if (status instanceof FooTable.Filter){
			this.$status.val(status.query.val());
		} else {
			this.$status.val(this.statusDefault);
		}

		// handle the jobTitle filter if one is supplied
		var jobTitle = this.find('status');
		if (jobTitle instanceof FooTable.Filter){
			this.$jobTitle.val(jobTitle.query.val());
		} else {
			this.$jobTitle.val(this.jobTitleDefault);
		}
	}
});

$(function() {
    $('.adv-table1').footable({
      filtering: {
        enabled: true
      },
      "paging": {
              "enabled": true,
			  "current": 1
	  },
      strings: {
        enabled: false
      },
      "filtering": {
              "enabled": true
          },
      components: {
          filtering: FooTable.MyFiltering
      },
    }); 
  });
  
FooTable.MyFiltering = FooTable.Filtering.extend({
	construct: function(instance){
		this._super(instance);
		// props for the first dropdown
		this.statuses = ['Web Developer1','Senior Manager','UX/UI Desogner','Content Writer','Graphic Designer','Marketer','Project Manager','UI Designer','Business Development'];
		this.statusDefault = 'kunlar';
		this.$status = null;
		// props for the second dropdown
		this.statuses1 = ['Active','deactivate','Blocked'];
		this.statusDefault1 = 'Status';
		this.$status = null;
		// props for the theerd dropdown
		this.jobTitles1 = ['Active1','deactivate1','Blocked1'];
		this.jobTitleDefault1 = "O'qituvchi";
		this.$jobTitle1 = null;
			// props for the theerd dropdown
			this.jobTitles = ['Active1','deactivate1','Blocked1'];
			this.jobTitleDefault = "kurslari";
			this.$jobTitle = null;
	},
	$create: function(){
		this._super();
		var self = this;
		// create the status form group and dropdown
		var $status_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position my-md-10 my-10 mr-sm-20 mr-0 '})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);

		self.$status = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onStatusDropdownChanged)
			.append($('<option/>', {text: self.statusDefault}))
			.appendTo($status_form_grp);

		$.each(self.statuses, function(i, status){
			self.$status.append($('<option/>').text(status));
		});



		// create the job title form group and dropdown
		var $job_title_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__status my-md-10 mt-10 mb-0 mr-sm-10 mr-0'})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);

		self.$jobTitle = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onJobTitleDropdownChanged)
			.append($('<option/>', {text: self.jobTitleDefault}))
			.appendTo($job_title_form_grp);

		$.each(self.jobTitles, function(i, jobTitle){
			self.$jobTitle.append($('<option/>').text(jobTitle));
		});


		// create the teacher title form group and dropdown
		var $job_title_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__status my-md-10 mt-10 mb-0 mr-sm-10 mr-0'})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);

		self.$jobTitle1 = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onJobTitleDropdownChanged)
			.append($('<option/>', {text: self.jobTitleDefault1}))
			.appendTo($job_title_form_grp);

		$.each(self.jobTitles1, function(i, jobTitle){
			self.$jobTitle1.append($('<option/>').text(jobTitle));
		});
		
		// create the status form group and dropdown
		var $status_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position my-md-10 my-10 mr-sm-10 mr-0 '})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);

		self.$status1 = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onStatusDropdownChanged)
			.append($('<option/>', {text: self.statusDefault1}))
			.appendTo($status_form_grp);

		$.each(self.statuses1, function(i, status){
			self.$status1.append($('<option/>').text(status));
		});
	},
	_onStatusDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.statusDefault){
			self.addFilter('position', selected, ['position']);
		} else {
			self.removeFilter('position');
		}
		self.filter();
	},
	_onJobTitleDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.jobTitleDefault){
			self.addFilter('status', selected, ['status']);
		} else {
			self.removeFilter('status');
		}
		self.filter();
	},
	draw: function(){
		this._super();
		// handle the status filter if one is supplied
		var status = this.find('position');
		if (status instanceof FooTable.Filter){
			this.$status.val(status.query.val());
		} else {
			this.$status.val(this.statusDefault);
		}

		// handle the jobTitle filter if one is supplied
		var jobTitle = this.find('status');
		if (jobTitle instanceof FooTable.Filter){
			this.$jobTitle.val(jobTitle.query.val());
		} else {
			this.$jobTitle.val(this.jobTitleDefault);
		}

		// handle the jobTitle1 filter if one is supplied
		var jobTitle1 = this.find('status');
		if (jobTitle1 instanceof FooTable.Filter){
			this.$jobTitle1.val(jobTitle1.query.val());
		} else {
			this.$jobTitle1.val(this.jobTitleDefault1);
		}
	}
});

$(function() {
    $('.adv-table2').footable({
      filtering: {
        enabled: true
      },
      "paging": {
              "enabled": true,
			  "current": 1
	  },
      strings: {
        enabled: false
      },
      "filtering": {
              "enabled": true
          },
      components: {
          filtering: FooTable.MyFiltering
      },
    }); 
  });
  
FooTable.MyFiltering = FooTable.Filtering.extend({
	construct: function(instance){
		this._super(instance);

		// props for the second dropdown
		this.jobTitles = ['Active','deactivate','Blocked'];
		this.jobTitleDefault = 'Status';
		this.$jobTitle = null;
	},
	$create: function(){
		this._super();
		var self = this;
		// create the status form group and dropdown
	


		// create the job title form group and dropdown
		var $job_title_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__status my-md-10 mt-10 mb-0 mr-sm-30 mr-0'})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);

		self.$jobTitle = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onJobTitleDropdownChanged)
			.append($('<option/>', {text: self.jobTitleDefault}))
			.appendTo($job_title_form_grp);

		$.each(self.jobTitles, function(i, jobTitle){
			self.$jobTitle.append($('<option/>').text(jobTitle));
		});
	},
	_onStatusDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.statusDefault){
			self.addFilter('position', selected, ['position']);
		} else {
			self.removeFilter('position');
		}
		self.filter();
	},
	_onJobTitleDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.jobTitleDefault){
			self.addFilter('status', selected, ['status']);
		} else {
			self.removeFilter('status');
		}
		self.filter();
	},
	draw: function(){
		this._super();
		// handle the status filter if one is supplied
		var status = this.find('position');
		if (status instanceof FooTable.Filter){
			this.$status.val(status.query.val());
		} else {
			this.$status.val(this.statusDefault);
		}

		// handle the jobTitle filter if one is supplied
		var jobTitle = this.find('status');
		if (jobTitle instanceof FooTable.Filter){
			this.$jobTitle.val(jobTitle.query.val());
		} else {
			this.$jobTitle.val(this.jobTitleDefault);
		}
	}
});
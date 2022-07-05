$(function() {
    $('.adv-table-group').footable({
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
		this.statusDefault = 'Status';
		this.$status = null;
		// courses
		this.courses = ['IT','English','Math'];
		this.courseDefault = 'Kurslar';
		this.$course = null;
		//teacher
		this.teachers = ['Aziz','Burhon','Jonibek'];
		this.teacherDefault = 'Oqituvchi';
		this.$teacher = null;
		//day
		this.days = ['dushanba','seshanba','chorshanba','payshanba','juma','shanba','yakshanba'];
		this.dayDefault = 'kunlar';
		this.$day = null;
	},
	$create: function(){
		this._super();
		var self = this;
		// create the status form group and dropdown
		var $status_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position '})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);

		self.$status = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onStatusDropdownChanged)
			.append($('<option/>', {text: self.statusDefault}))
			.appendTo($status_form_grp);

		$.each(self.statuses, function(i, status){
			self.$status.append($('<option/>').text(status));
		});


		// courses
		var $course_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position'})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);

		self.$course = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onCourseDropdownChanged)
			.append($('<option/>', {text: self.courseDefault}))
			.appendTo($course_form_grp);

		$.each(self.courses, function(i, status){
			self.$course.append($('<option/>').text(status));
		});
		
		//teacher 
		var $teacher_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position'})
		.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
		.prependTo(self.$form);

	self.$teacher = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
		.on('change', {self: self}, self._onTeacherDropdownChanged)
		.append($('<option/>', {text: self.teacherDefault}))
		.appendTo($teacher_form_grp);

	$.each(self.teachers, function(i, status){
		self.$teacher.append($('<option/>').text(status));
	});

			//day
			var $day_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position'})
			.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
			.prependTo(self.$form);
	
		self.$day = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
			.on('change', {self: self}, self._onDayDropdownChanged)
			.append($('<option/>', {text: self.dayDefault}))
			.appendTo($day_form_grp);
	
		$.each(self.days, function(i, status){
			self.$day.append($('<option/>').text(status));
		});
	},
	_onStatusDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.jobTitleDefault){
			self.addFilter('status', selected, ['status']);
		} else {
			self.removeFilter('status');
		}
		self.filter();
	},

	_onCourseDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.courseDefault){
			self.addFilter('course', selected, ['course']);
		} else {
			self.removeFilter('course');
		}
		self.filter();
	},

	_onTeacherDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.teacherDefault){
			self.addFilter('teacher', selected, ['teacher']);
		} else {
			self.removeFilter('teacher');
		}
		self.filter();
	},

	_onDayDropdownChanged: function(e){
		var self = e.data.self,
			selected = $(this).val();
		if (selected !== self.dayDefault){
			self.addFilter('day', selected, ['day']);
		} else {
			self.removeFilter('day');
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

		// handle the course filter if one is supplied
		var course = this.find('course');
		if (course instanceof FooTable.Filter){
			this.$course.val(status.query.val());
		} else {
			this.$course.val(this.courseDefault);
		}

		 // handle the teacher filter if one is supplied
				var teacher = this.find('teacher');
				if (teacher instanceof FooTable.Filter){
					this.$teacher.val(status.query.val());
				} else {
					this.$teacher.val(this.teacherDefault);
				}
	
		 // handle the day filter if one is supplied
		 var day = this.find('day');
		 if (day instanceof FooTable.Filter){
			 this.$day.val(status.query.val());
		 } else {
			 this.$day.val(this.dayDefault);
		 }
	}
});

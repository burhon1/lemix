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
		this.teacherDefault = "O'qituvchi";
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






//course detail
$(function() {
    $('.adv-table-course-detail').footable({
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
          filtering: FooTable.CourseDetail
      },
    }); 
  });
  
FooTable.CourseDetail = FooTable.Filtering.extend({
	construct: function(instance){
		this._super(instance);
		// props for the first dropdown
		this.statuses = ['Web Developer','Senior Manager','UX/UI Desogner','Content Writer','Graphic Designer','Marketer','Project Manager','UI Designer','Business Development'];
		this.statusDefault = 'Barchasi';
		this.$status = null;
		// courses
		this.courses = ['10:10 12:00','English','Math'];
		this.courseDefault = 'Vaqt';
		this.$course = null;
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
	

			//day

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
		
	}
});












//Roomslist


$(function() {
    $('.adv-table-rooms-list').footable({
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
          filtering: FooTable.Rooms_listDetail
      },
    }); 
  });
  
FooTable.Rooms_listDetail = FooTable.Filtering.extend({
	construct: function(instance){
		this._super(instance);
		// props for the first dropdown
	
	}})

















	//Teachers-LIst
$(function() {
    $('.adv-table-teachers-list').footable({
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
          filtering: FooTable.TeachersDetail
      },
    }); 
  });
  
FooTable.TeachersDetail = FooTable.Filtering.extend({
	construct: function(instance){
		this._super(instance);
		// props for the first dropdown
		this.statuses = ['Web Developer','Senior Manager','UX/UI Desogner','Content Writer','Graphic Designer','Marketer','Project Manager','UI Designer','Business Development'];
		this.statusDefault = 'Status';
		this.$status = null;
	
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

	


	
	
	draw: function(){
		this._super();
		// handle the status filter if one is supplied
		var status = this.find('position');
		if (status instanceof FooTable.Filter){
			this.$status.val(status.query.val());
		} else {
			this.$status.val(this.statusDefault);
		}



		
	}
});


















//courses  list
$(function() {
    $('.adv-table-course-list').footable({
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
          filtering: FooTable.CoursesDetail
      },
    }); 
  });
  
FooTable.CoursesDetail = FooTable.Filtering.extend({
	construct: function(instance){
		this._super(instance);
	// courses
		this.courses = ['nima','yozish','kerak'];
		this.courseDefault = 'Davomiyligi';
		this.$course = null;
		// props for the first dropdown
		this.statuses = ['Web Developer','Senior Manager','UX/UI Desogner','Content Writer','Graphic Designer','Marketer','Project Manager','UI Designer','Business Development'];
		this.statusDefault = 'Statusi';
		this.$status = null;
		
		
	},
	$create: function(){
		this._super();
		var self = this;
	

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
		
	}
});

















//employes  list
$(function() {
    $('.adv-table-employees-list').footable({
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
          filtering: FooTable.EmployeesDetail
      },
    }); 
  });
  
FooTable.EmployeesDetail = FooTable.Filtering.extend({
	construct: function(instance){
		this._super(instance);
	// courses
		this.courses = ['Active','Deactive','banned'];
		this.courseDefault = 'Activate';
		this.$course = null;
		// props for the first dropdown
	
		
		
	},
	$create: function(){
		this._super();
		var self = this;
	

		// activate
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

	
	
	draw: function(){
		this._super();
	

		// handle the course filter if one is supplied
		var course = this.find('course');
		if (course instanceof FooTable.Filter){
			this.$course.val(status.query.val());
		} else {
			this.$course.val(this.courseDefault);
		}

	}
});





















//students list 
$(function() {
    $('.adv-table-students').footable({
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
		
		// courses
		this.courses = ['IT','English','Math'];
		this.courseDefault = 'Kurslar';
		this.$course = null;
			//groups
			this.groups = ['Aziz','Burhon','Jonibek'];
			this.groupDefault = 'Guruhlar';
			this.$group = null;
		//teacher
		this.teachers = ['Aziz','Burhon','Jonibek'];
		this.teacherDefault = "O'qituvchi";
		this.$teacher = null;
		//day
		// this.days = ['dushanba','seshanba','chorshanba','payshanba','juma','shanba','yakshanba'];
		// this.dayDefault = 'Holati';
		// this.$day = null;
		//      hols
		// 	this.hols = ['dushanba','seshanba','chorshanba','payshanba','juma','shanba','yakshanba'];
		// 	this.holDefault = 'Moliyaviy Holati';
		// 	this.$hol = null;
	},
	$create: function(){
		this._super();
		var self = this;



		

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
		

				//groups
				var $group_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position'})
				.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
				.prependTo(self.$form);
		
			self.$group = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
				.on('change', {self: self}, self._onGroupDropdownChanged)
				.append($('<option/>', {text: self.groupDefault}))
				.appendTo($group_form_grp);
		
			$.each(self.groups, function(i, status){
				self.$group.append($('<option/>').text(status));
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

					// 	// create the hol form group and dropdown
					// 	var $hol_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position '})
					// 	.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
					// 	.prependTo(self.$form);
		
					// self.$hol = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
					// 	.on('change', {self: self}, self._onHolDropdownChanged)
					// 	.append($('<option/>', {text: self.holDefault}))
					// 	.appendTo($hol_form_grp);
		
					// $.each(self.hols, function(i, status){
					// 	self.$hol.append($('<option/>').text(status));
					// });
		
	},


	

	_onGroupDropdownChanged: function(e){
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


	// _onHolDropdownChanged: function(e){
	// 	var self = e.data.self,
	// 		selected = $(this).val();
	// 	if (selected !== self.jobTitleDefault){
	// 		self.addFilter('status', selected, ['status']);
	// 	} else {
	// 		self.removeFilter('status');
	// 	}
	// 	self.filter();
	// },
	
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

		// handle the group filter if one is supplied
		var course = this.find('group');
		if (course instanceof FooTable.Filter){
			this.$group.val(status.query.val());
		} else {
			this.$group.val(this.groupDefault);
		}

		 // handle the teacher filter if one is supplied
				var teacher = this.find('teacher');
				if (teacher instanceof FooTable.Filter){
					this.$teacher.val(status.query.val());
				} else {
					this.$teacher.val(this.teacherDefault);
				}


				 // handle the hol filter if one is supplied
				 var hol = this.find('teacher');
				 if (hol instanceof FooTable.Filter){
					 this.$hol.val(status.query.val());
				 } else {
					 this.$hol.val(this.holDefault);
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














//expenses


$(function() {
    $('.adv-table-expenses').footable({
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
		
		// courses
		this.courses = ['IT','English','Math'];
		this.courseDefault = 'Kurslar';
		this.$course = null;
			//groups
			this.groups = ['Aziz','Burhon','Jonibek'];
			this.groupDefault = 'Guruhlar';
			this.$group = null;
		//teacher
		this.teachers = ['Aziz','Burhon','Jonibek'];
		this.teacherDefault = "O'qituvchi";
		this.$teacher = null;
		//day
		this.days = ['dushanba','seshanba','chorshanba','payshanba','juma','shanba','yakshanba'];
		this.dayDefault = 'Holati';
		this.$day = null;
		     //hols
			
	},
	$create: function(){
		this._super();
		var self = this;



		

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
		

				//groups
				var $group_form_grp = $('<div/>', {'class': 'form-group atbd-select d-flex align-items-center adv-table-searchs__position mr-sm-0'})
				.append($('<label/>', {'class': 'd-flex align-items-center mb-sm-0 mb-2', text: ''}))
				.prependTo(self.$form);
		
			self.$group = $('<select/>', { 'class': 'form-control ml-sm-10 ml-0' })
				.on('change', {self: self}, self._onGroupDropdownChanged)
				.append($('<option/>', {text: self.groupDefault}))
				.appendTo($group_form_grp);
		
			$.each(self.groups, function(i, status){
				self.$group.append($('<option/>').text(status));
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


	

	_onGroupDropdownChanged: function(e){
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

		// handle the group filter if one is supplied
		var course = this.find('group');
		if (course instanceof FooTable.Filter){
			this.$group.val(status.query.val());
		} else {
			this.$group.val(this.groupDefault);
		}

		 // handle the teacher filter if one is supplied
				var teacher = this.find('teacher');
				if (teacher instanceof FooTable.Filter){
					this.$teacher.val(status.query.val());
				} else {
					this.$teacher.val(this.teacherDefault);
				}


				 // handle the hol filter if one is supplied
				 var hol = this.find('teacher');
				 if (hol instanceof FooTable.Filter){
					 this.$hol.val(status.query.val());
				 } else {
					 this.$hol.val(this.holDefault);
				 }
	
		 // handle the day filter if one is supplied
	
	}
});



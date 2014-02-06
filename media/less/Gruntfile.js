module.exports = function(grunt) {
  "use strict";

  // Project configuration.
  grunt.initConfig({
    jqueryCheck: 'if (!jQuery) { throw new Error(\"Bootstrap requires jQuery\") }\n\n',

    recess: {
      options: {
        compile: true
      },
      base: {
        options: {
          compress: true
        },
        src: ['base.less'],
        dest: '../css/base.min.css'
      },
      user_merits: {
        options: {
          compress: true
        },
        src: ['user_merits.less'],
        dest: '../css/user_merits.min.css'
      }
    },

    watch: {
      recess: {
        files: ['*.less', 'bootstrap/less/*.less'],
        tasks: ['recess']
      }
    }
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-recess');

  // CSS distribution task.
  grunt.registerTask('compile-css', ['recess']);

  // Default task.
  grunt.registerTask('default', ['compile-css']);
};

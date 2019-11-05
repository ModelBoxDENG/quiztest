<template>
<div class="questionBox" id="aqq">
	  <!-- transition -->
	  		<transition :duration="{ enter: 500, leave: 300 }" enter-active-class="animated zoomIn" leave-active-class="animated zoomOut" mode="out-in">
	  <!--qusetionContainer-->
	  			<div class="questionContainer" v-if="questionIndex<quiz.questions.length" v-bind:key="questionIndex">

	  				<header>
	  					<h1 class="title is-6">Quiz</h1>
	  					<!--progress-->
	  					<div class="progressContainer">
	  						<progress class="progress is-info is-small" :value="(questionIndex/quiz.questions.length)*100" max="100">{{(questionIndex/quiz.questions.length)*100}}%</progress>
	  						<p>{{(questionIndex/quiz.questions.length)*100}}% complete</p>
	  					</div>
	  					<!--/progress-->
	  				</header>

	  				<!-- questionTitle -->
	  				<h2 class="titleContainer title">{{ quiz.questions[questionIndex].text }}</h2>

	  				<!-- quizOptions -->
	  				<div class="optionContainer">
	  					<div class="option" v-for="(response, index) in quiz.questions[questionIndex].responses"  :class="(userClicked.includes(index))? (quiz.questions[questionIndex].responses[index].correct == true? 'is-selected_correct':'is-selected_wrong'): ''" :key="index" @click="selectOption(index)">
	  						{{ index | charIndex }}. {{ response.text }}
	  					</div>
	  				</div>

	  				<!--quizFooter: navigation and progress-->
	  				<footer class="questionFooter">

	  					<!--pagination-->
	  					<nav class="pagination" role="navigation" aria-label="pagination">

	  						<!-- back button -->
	  						<a class="button" v-on:click="prev();" :disabled="questionIndex < 1">
								Back
							</a>

	  						<!-- next button -->
	  						<a class="button" :class="(userResponses[questionIndex]==null)?'':'is-active'" v-on:click="next();" :disabled="questionIndex>=quiz.questions.length">
	                      {{ (userResponses[questionIndex]==null)?'Skip':'Next' }}
	                    </a>

	  					</nav>
	  					<!--/pagination-->

	  				</footer>
	  				<!--/quizFooter-->

	  			</div>
				<!--quizCompletedResult-->
					<div v-if="questionIndex >= quiz.questions.length" v-bind:key="questionIndex" class="quizCompleted has-text-centered">

						<!-- quizCompletedIcon: Achievement Icon -->
						<span class="icon">
						<i class="fa" :class="score()>3?'fa-check-circle-o is-active':'fa-times-circle'"></i>
					  </span>

						<!--resultTitleBlock-->
						<h2 class="title">
							You did {{ (score()>7?'an amazing': (score()< 4 ?'a poor':'a good')) }} job!
						</h2>
						<p class="subtitle">
							Total score: {{ score() }} / {{ quiz.questions.length }}
						</p>
							<br>
							<a class="button" @click="restart()">restart <i class="fa fa-refresh"></i></a>
						<!--/resultTitleBlock-->

					</div>
					<!--/quizCompetedResult-->
	  		</transition>
	</div>
</template>

<script>
  //	<div class="option" v-for="(response, index) in quiz.questions[questionIndex].responses" @click="selectOption(index)" :class="ifUserClicked?((userResponses[questionIndex] == index)? (quiz.questions[questionIndex].responses[index].correct == true? 'is-selected_correct':'is-selected_wrong'): ''):''" :key="index">
import Vue from '../../static/utils/vue.js';
//只需要更改quiz的内容就可以改题目了
var max_question = 10;//默认quiz最大题目数量
var questions = require('../../static/sample_data_look.json');
var user_data_look = require('../../static/user_data_look.json');
//
      //根据用户答题情况，减去题目。
//-----------------------------------//
//在questions题库内随机挑max_question个题目,并且输出new_quiz
var arr = [];
for (var i = 0; i <=questions.length-1; i++) { arr.push(i); }
arr.sort(
    function () {
        return 0.5 - Math.random();
    }
);
arr.length = max_question;
var new_quiz = [];
arr.forEach(function(element) {
  new_quiz.push(questions[element]);
});
//-----------------------------------//

//从new_quiz提取question_id,question_text
var arr_question_id = [];
var arr_question_text = [];
var arr_response_text = [];
new_quiz.forEach(function(ele){
  arr_question_id.push(ele.question_id);
  arr_question_text.push(ele.question);
  arr_response_text.push(ele.responses.sort(function() {
    return .5 - Math.random();
  }));
});
//-----------------------------------//
class Questions {
  constructor(text, responses) {
    this.text = text;
    this.responses = responses;
  }
}
var questions = [];
for(var i =0; i <=arr_question_id.length-1; i++){
  questions.push(new Questions(arr_question_text[i], arr_response_text[i]));
}

class Quiz {
  constructor(user, questions) {
    this.user = user;
    this.questions = questions;
  }
}

var quiz = new Quiz('Dave', questions),
userResponseSkelaton = Array(quiz.questions.length).fill(null);


//var quiz = {
//      user: "Dave",
//      questions: [
//         {
//            text: "What is the full form of HTTP?",
//            responses: [
//               { text: "Hyper text transfer package", correct: true },
//               { text: "Hyper text transfer protocol", correct: true },
//            ]
//         },
//      ]
//   },
//   userResponseSkelaton = Array(quiz.questions.length).fill(null);

export default {
  name: "aqq",
  data () {
    return {
      quiz: quiz,
      questionIndex: 0,
      userResponses: userResponseSkelaton,
      isActive: false,
      lastindex: 0,
      userClicked:[],
      ifUserClicked:false,
      ifmultiple:false,
      selectedIndex:-1,
    }
  },

  filters: {
      charIndex: function(i) {
         return String.fromCharCode(97 + i);
      }
   },
   methods: {
		 restart: function(){
			 	this.questionIndex=0;
		 		this.userResponses=Array(this.quiz.questions.length).fill(null);
		 },

      selectOption: function(index) {
        this.selectedIndex = index;

        let idx = this.userClicked.indexOf(index);
        //如果已经选中了，那就取消选中，如果没有，则选中
        if(idx>-1){
          //取消选中
          this.userClicked.splice(idx,1);
          //取消错误答案的时候，打乱顺序。
          if (this.quiz.questions[this.questionIndex].responses[index].correct==undefined){
            //清空选择\
            this.userClicked=[];
            this.userResponses[this.questionIndex]=null;
            this.selectedIndex=-1;
            //打乱顺序
            this.quiz.questions[this.questionIndex].responses.sort(function() {
              return .5 - Math.random();
            });

          }


        }else{
          //选中
          this.userClicked.push(index);
        }
        Vue.set(this.userResponses, this.questionIndex, this.userClicked);
        this.lastindex = index;





      },

      numOfCorrect: function(index){
        let num = 0;
        for (let text in quiz.questions[index].responses){
          if (quiz.questions[index].responses[text].correct!=null){
            num = num+1;
          }
        }
        return num;
      },
      next: function() {
        this.userClicked=[];
         if (this.questionIndex < this.quiz.questions.length)
            this.questionIndex++;
      },

      prev: function() {
         if (this.quiz.questions.length > 0) this.questionIndex--;
      },
      // Return "true" count in userResponses
      score: function() {
        //this.quiz.questions[this.questionIndex].responses 和userreponse做对比
         var score = 0;
         var flag = true;
         for (var i = 0; i < this.userResponses.length; i++) {
           flag = true;
           for (var j = 0; j<this.userResponses[i].length;j++){
             if (this.quiz.questions[i].responses[j].correct == undefined){
               flag = false;
               break;
             }
           }
           if (flag == true){
             score = score + 1;
           }

         }
         return score;
      }
   }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import '../assets/css.CSS';
</style>

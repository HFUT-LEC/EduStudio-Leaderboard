<template>
  <div class="home">
    <div class="container">
      <h4>Welcome to Result Presentation Leaderboard of Edustudio</h4>
      <p class="text-start hint-text">Please select Task supported by EduStudio. And then all results would be displayed.</p>
      <LeaderBoardSelect
        @refresh="refresh"
        :showContext="showContext"
      />
      <LeaderBoardResult
        @metric_selectAll="metric_selectAll"
        @metric_selectPart="metric_selectPart"
        @metric_show="metric_show"
        @metric_unshow="metric_unshow"
        @fold_selectAll="fold_selectAll"
        @fold_selectPart="fold_selectPart"
        @fold_show="fold_show"
        @fold_unshow="fold_unshow"
        @model_selectAll="model_selectAll"
        @model_selectPart="model_selectPart"
        @model_show="model_show"
        @model_unshow="model_unshow"
        :dataInfo="dataInfo"
        :model_state="model_state"
        :fold_state_father="fold_state_father"
        :metric_state_father="metric_state_father"
      />
    </div>
  </div>
</template>

<script>
import LeaderBoardSelect from "@/components/LeaderBoardSelect"
import LeaderBoardResult from "@/components/LeaderBoardResult"
import $ from "jquery"
import { reactive, computed, inject } from "vue"

export default {
  name: "LeaderBoardView",
  components: {
    LeaderBoardSelect,
    LeaderBoardResult,
  },
  setup() {
    const showContext = reactive({
      is_showed: false,
      task: "None",
      dataset: "None",
      application: "None",
      taskID: { CognitiveDiagnosis: 1, KnowledgeTracing: 2 },
      datasetID: { FrcSub: 1, ASSISTment0910: 2, Junyi: 3 },
      applicationID: { General: 1, KnowledgeMissing: 2 },
    })
    const dataInfo = reactive({
      is_showed: false,
      model_icon_is_showed: true,
      models: [
        {
          id: 1,
          model: "IRT",
        },
        {
          id: 2,
          model: "NCDM",
        },
        {
          id: 3,
          model: "KaNCD",
        },
        {
          id: 4,
          model: "KSCD",
        },
        {
          id: 5,
          model: "RCD",
        },
      ],
      fold_icon_is_showed: false,
      folds: [
        {
          id: 101,
          fold: "One",
        },
        {
          id: 102,
          fold: "Five",
        },
      ],
      metric_icon_is_showed: false,
      metrics: [
        {
          id: 201,
          metric: "AUC",
        },
        {
          id: 202,
          metric: "RMSE",
        },
        {
          id: 203,
          metric: "ACC",
        },
      ],
      data_source: [],
    })
    const model_state = reactive({
      allSelected: false,
      indeterminate: false,
      selct: [],
    })
    const fold_state_father = reactive({
      allSelected: false,
      selct: -1,
    })
    const metric_state_father = reactive({
      allSelected: false,
      indeterminate: false,
      selct: [],
    })
  
    const currentSortedKey = inject('currentSortedKey', () => {
      throw new Error('currentSortedKey injection failed'); // 确保注入成功
    });
    const changeValue = () => {
      currentSortedKey.value = 'TEST';
    }

    // 进行数据请求操作
    const refresh = async (selectedTask, selectedDataset) => {
      showContext.is_showed = true // 标志，是否展示数据部分的操作
      dataInfo.is_showed = true // 标志，是否展示数据展示操作部分
      showContext.task = selectedTask
      showContext.dataset = selectedDataset
      showContext.application = "General"
      // console.log(showContext.task, showContext.dataset, showContext.application);
      // 读取远程数据
      let optResult = computed(() => showContext.taskID[showContext.task] * 100 + showContext.datasetID[showContext.dataset] * 10 + showContext.applicationID[showContext.application])
      let optResultPath = "https://raw.githubusercontent.com/HFUT-LEC/EduStudio-Leaderboard/backend/results/result_" + optResult.value.toString() + ".json"
      const dt = await $.getJSON(optResultPath) // 利用asunc和await实现响应等待操作：后续的代码执行会等待回调函数$.getJSON()执行完成
      // console.log(dt);
      dataInfo.model_icon_is_showed = true // 设置重置数据类时, Model列自动展开
      dataInfo.models = dt.data.map((item) => ({ id: item.id, model: item.model }))
      dataInfo.data_source = dt.data
      // 设置初始模型选择的状态
      model_state.allSelected = true
      model_state.indeterminate = false
      model_state.selct = dataInfo.models.map((mo) => mo.id)
      // 设置初始Fold的状态
      fold_state_father.allSelected = true
      fold_state_father.selct = dataInfo.folds[0].id
      // 设置初始Metric的状态
      metric_state_father.allSelected = true
      metric_state_father.indeterminate = false
      metric_state_father.selct = [dataInfo.metrics[0].id, dataInfo.metrics[1].id]

      changeValue()
    }
    // 利用UI选择的评估指标进行数据筛选
    const metric_selectPart = (data) => {
      if (data.length && data.length > 2) {
        alert('仅支持选择两个Metric选项，多于两个只保留上两个已选选项');

        // 如果选中的选项数量超过两个，只保留前两个选项
        metric_state_father.selct = data.slice(0, 2);
      } else {
        metric_state_father.allSelected = false
        metric_state_father.indeterminate = true
        metric_state_father.selct = data
      }
    }
    const metric_selectAll = (data) => {
      if (data) {
        metric_state_father.selct = [dataInfo.metrics[0].id, dataInfo.metrics[1].id]
        metric_state_father.allSelected = true
        metric_state_father.indeterminate = false
      } else {
        metric_state_father.selct = []
        metric_state_father.allSelected = false
      }
    }
    const metric_show = () => {
      if (dataInfo.metric_icon_is_showed) return
      dataInfo.metric_icon_is_showed = true
    }
    const metric_unshow = () => {
      if (!dataInfo.metric_icon_is_showed) return
      dataInfo.metric_icon_is_showed = false
    }
    // 利用UI选择的交叉验证进行数据筛选
    const fold_selectPart = (data) => {
      fold_state_father.allSelected = true
      fold_state_father.selct = data
    }
    const fold_selectAll = (data) => {
      if (data) {
        fold_state_father.allSelected = true
        fold_state_father.selct = dataInfo.folds[0].id
      } else {
        fold_state_father.allSelected = false
        fold_state_father.selct = -1
      }
    }
    const fold_show = () => {
      if (dataInfo.fold_icon_is_showed) return
      dataInfo.fold_icon_is_showed = true
    }
    const fold_unshow = () => {
      if (!dataInfo.fold_icon_is_showed) return
      dataInfo.fold_icon_is_showed = false
    }
    // 利用UI选择的模型进行数据筛选
    const model_selectPart = (data) => {
      if (data.length && data.length == dataInfo.models.length) {
        model_state.allSelected = true
        model_state.indeterminate = false
        model_state.selct = data
      } else if (data.length && data.length != dataInfo.models.length) {
        model_state.allSelected = false
        model_state.indeterminate = true
        model_state.selct = data
      } else {
        model_state.indeterminate = false
        model_state.selct = []
      }
    }
    const model_selectAll = (data) => {
      if (data) {
        model_state.selct = dataInfo.models.map((mo) => mo.id)
        model_state.allSelected = true
        model_state.indeterminate = false
      } else {
        model_state.selct = []
        model_state.allSelected = false
      }
    }
    const model_show = () => {
      if (dataInfo.model_icon_is_showed) return
      dataInfo.model_icon_is_showed = true
    }
    const model_unshow = () => {
      if (!dataInfo.model_icon_is_showed) return
      dataInfo.model_icon_is_showed = false
    }

    return {
      showContext,
      dataInfo,
      model_state,
      fold_state_father,
      metric_state_father,
      refresh,
      metric_show,
      metric_unshow,
      metric_selectPart,
      metric_selectAll,
      fold_show,
      fold_unshow,
      fold_selectPart,
      fold_selectAll,
      model_show,
      model_unshow,
      model_selectPart,
      model_selectAll,
    }
  },
}
</script>

<style scoped>
.hint-text {
  margin-bottom: 5px;
  margin-top: 40px;
  font-size: small;
  color: grey;
}

h4 {
  font-weight: bold;
  text-align: center;
}

.container {
  margin-top: 20px;
}
</style>

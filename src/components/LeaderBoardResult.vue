<template>
  <div
    v-if="dataInfo.is_showed"
    class="card card-result-home"
  >
    <div class="card-body">
      <!-- 操作选择 -->
      <h3>Listed Operations and Metrics</h3>
      <div class="om-select-list">
        <!-- 模型选择 -->
        <div>
          <div class="row check-all">
            <div class="col-auto om-col-auto-form-check">
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  v-model="modelState_change.allSelected"
                  @change="model_selectAll"
                  id="model-check-all"
                  :indeterminate="model_state.indeterminate"
                />
                <label
                  class="form-check-label"
                  for="model-check-all"
                  >Model</label
                >
              </div>
            </div>
            <div class="col-auto om-col-auto-icon">
              <svg
                @click="model_show"
                v-if="!dataInfo.model_icon_is_showed"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-caret-down"
                viewBox="0 0 16 16"
              >
                <path d="M3.204 5h9.592L8 10.481 3.204 5zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659z" />
              </svg>
              <svg
                @click="model_unshow"
                v-if="dataInfo.model_icon_is_showed"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-caret-up"
                viewBox="0 0 16 16"
              >
                <path d="M3.204 11h9.592L8 5.519 3.204 11zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659z" />
              </svg>
            </div>
          </div>
          <div
            v-if="dataInfo.model_icon_is_showed"
            class="card icon-check-list"
          >
            <div class="card-body om-card-body-content">
              <div
                v-for="mo in dataInfo.models"
                :key="mo.id"
                class="form-check form-check-inline"
              >
                <input
                  v-model="modelState_change.selct"
                  class="form-check-input"
                  type="checkbox"
                  :id="mo.id"
                  :value="mo.id"
                  @change="model_selectPart"
                />
                <label
                  class="form-check-label"
                  :for="mo.id"
                  >{{ mo.model }}</label
                >
              </div>
            </div>
          </div>
        </div>

        <!-- 交叉验证 -->
        <!-- <div>
          <div class="row check-all">
            <div class="col-auto om-col-auto-form-check">
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  v-model="fold_state.allSelected"
                  @change="fold_selectAll"
                  id="fold-check-all"
                />
                <label class="form-check-label" for="fold-check-all">Fold</label>
              </div>
            </div>
          </div>
          <div class="card icon-check-list">
            <div class="card-body om-card-body-content">
              <div v-for="fo in dataInfo.folds" :key="fo.id" class="form-check form-check-inline">
                <input
                  v-model="fold_state.selct"
                  class="form-check-input"
                  type="radio"
                  :id="fo.id"
                  :value="fo.id"
                  @change="fold_selectPart"
                />
                <label class="form-check-label" :for="fo.id">{{ fo.fold }}</label>
              </div>
            </div>
          </div>
        </div> -->

        <!-- 评估指标选择 -->
        <div>
          <div class="row check-all">
            <div class="col-auto om-col-auto-form-check">
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  v-model="metric_state.allSelected"
                  @change="metric_selectAll"
                  id="metric-check-all"
                  :indeterminate="metric_state.indeterminate"
                />
                <label class="form-check-label" for="metric-check-all">Metric</label>
              </div>
            </div>
          </div>
          <div class="card icon-check-list">
            <div class="card-body om-card-body-content">
              <div v-for="me in dataInfo.metrics" :key="me.id" class="form-check form-check-inline">
                <input
                  v-model="metric_state.selct"
                  class="form-check-input"
                  type="checkbox"
                  :id="me.id"
                  :value="me.id"
                  @change="metric_selectPart"
                />
                <label class="form-check-label" :for="me.id">{{ me.metric }}</label>
              </div>
            </div>
          </div>
        </div>
        <!-- <div>
          {{ model_state.selct }}
        </div>
        -->
      </div>
      <div style="text-align: center;font-size: 20px;"> Sorted benchmarking results by {{ currentSortedKey }}</div>
      <div
        ref="chartRef"
        style="width: 100%; height: 400px"
      ></div>
      <!-- 数据表格展示 -->
      <h3 style="margin-top: 15px">Presentation of Models' Results</h3>
      
      <div class="card model-result-show">
        <div class="card-body">
          <!-- <input v-model="searchText" placeholder="请输入搜索条件" /> -->
          <table class="table">
            <thead>
              <tr>
                <th
                  v-for="field in data_show_result.fixed_fields[1]"
                  :key="field.key"
                >
                  {{ field.label }}
                </th>
                <th
                  v-for="field in data_show_result.fields"
                  :key="field.key"
                >
                  <div style="display: flex; align-items: center; gap: 10px">
                    {{ field.label }}
                    <svg
                      @click="sortBy(field.key)"
                      v-if="!data_show_result.sortIcons[field.key]"
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-caret-down"
                      viewBox="0 0 16 16"
                    >
                      <path d="M3.204 5h9.592L8 10.481 3.204 5zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659z" />
                    </svg>
                    <svg
                      @click="sortBy(field.key)"
                      v-if="data_show_result.sortIcons[field.key] && data_show_result.sortOrders[field.key] == -1"
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-caret-down-fill"
                      viewBox="0 0 16 16"
                    >
                      <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z" />
                    </svg>
                    <svg
                      @click="sortBy(field.key)"
                      v-if="data_show_result.sortIcons[field.key] && data_show_result.sortOrders[field.key] == 1"
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-caret-up-fill"
                      viewBox="0 0 16 16"
                    >
                      <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z" />
                    </svg>
                  </div>
                </th>
                <th
                  v-for="field in data_show_result.fixed_fields[0]"
                  :key="field.key"
                >
                  {{ field.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in sortedItems"
                :key="item.id"
              >
                <td
                  v-for="field in data_show_result.fixed_fields[1]"
                  :key="field.key"
                >
                  {{ item[field.key] }}
                </td>
                <td
                  v-for="field in data_show_result.fields"
                  :key="field.key"
                >
                  {{ item[field.key] }}
                </td>
                <td
                  v-for="field in data_show_result.fixed_fields[0]"
                  :key="field.key"
                >
                  <a
                    :href="getTruncatedUrl(item[field.logurl1])"
                    target="_blank"
                    v-if="fold_state.selct == 101"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-gear"
                      viewBox="0 0 16 16"
                    >
                      <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z" />
                      <path
                        d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"
                      />
                    </svg>
                  </a>
                  <a
                    :href="item[field.logurl2]"
                    target="_blank"
                    v-if="fold_state.selct == 102"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="currentColor"
                      class="bi bi-gear"
                      viewBox="0 0 16 16"
                    >
                      <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z" />
                      <path
                        d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"
                      />
                    </svg>
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, onMounted, computed, watch, provide } from "vue"
import * as echarts from "echarts"
export default {
  name: "LeaderBoardResult",
  props: {
    dataInfo: {
      type: Object,
      required: true,
    },
    model_state: {
      type: Object,
      required: true,
    },
    fold_state_father: {
      type: Object,
      required: true,
    },
    metric_state_father: {
      type: Object,
      required: true,
    },
  },
  watch: {
    // 初始化
    dataInfo: {
      handler(newVal) {
        if (newVal.is_showed) {
          // this.$nextTick(() => {
            this.drawChart()
          // })
        }
      },
      deep: true,
    },
    // 监听父组件中数据变化，然后进行不同的操作
    model_state: {
      handler(newVal) {
        console.log(newVal, "----------Model-newVal---------")
        console.log(this.dataInfo, "----------Model-props.dataInfo---------")
        this.modelState_change.allSelected = newVal.allSelected
        this.modelState_change.indeterminate = newVal.indeterminate
        this.modelState_change.selct = newVal.selct
        // 对选择的model进行排序
        let sortedmodel = computed(() => [...this.modelState_change.selct].sort((a, b) => a - b))
        this.data_show_result.items = [] // 每次点击将数据置空
        for (let idx = 0; idx < sortedmodel.value.length; idx++) {
          this.addRowItem(sortedmodel.value[idx])
        }

        console.log(this.data_show_result, "----------data_show_result---------")
      },
      deep: true,
    },
    fold_state_father: {
      handler(newVal) {
        console.log(newVal, "----------Fold-newVal---------")
        this.fold_state.allSelected = newVal.allSelected
        this.fold_state.selct = newVal.selct
        // 对选择的fold和metric进行排序
        let sortedmetric = computed(() => [...this.metric_state.selct].sort((a, b) => a - b))
        // 重写col name方式进行数据筛选
        this.data_show_result.fields = []
        for (let midx = 0; midx < sortedmetric.value.length; midx++) {
          let fnum = computed(() => sortedmetric.value[midx] * 10 + this.fold_state.selct)
          if (fnum.value == 2111) {
            this.addColField("auc-1", "AUC-1")
          } else if (fnum.value == 2121) {
            this.addColField("rmse-1", "RMSE-1")
          } else if (fnum.value == 2131) {
            this.addColField("acc-1", "ACC-1")
          } else if (fnum.value == 2112) {
            this.addColField("auc-5", "AUC-5")
          } else if (fnum.value == 2122) {
            this.addColField("rmse-5", "RMSE-5")
          } else if (fnum.value == 2132) {
            this.addColField("acc-5", "ACC-5")
          }
        }
        console.log(this.data_show_result, "-----------data_show_result.fields--------")
        this.redrawChart()
      },
      deep: true,
    },
    metric_state_father: {
      handler(newVal, oldVal, source) {
        console.log("Triggered by:", source)
        console.log(newVal, "----------metric-newVal---------")
        this.metric_state.allSelected = newVal.allSelected
        this.metric_state.indeterminate = newVal.indeterminate
        this.metric_state.selct = newVal.selct
        // 对col name进行排序
        let sortedmetric = computed(() => [...this.metric_state.selct].sort((a, b) => a - b))
        // 重写col name方式进行数据筛选
        this.data_show_result.fields = []
        for (let midx = 0; midx < sortedmetric.value.length; midx++) {
          if (this.fold_state.selct == -1) {
            break
          }
          let fnum = computed(() => sortedmetric.value[midx] * 10 + this.fold_state.selct)
          if (fnum.value == 2111) {
            this.addColField("auc-1", "AUC-1")
          } else if (fnum.value == 2112) {
            this.addColField("auc-5", "AUC-5")
          } else if (fnum.value == 2121) {
            this.addColField("rmse-1", "RMSE-1")
          } else if (fnum.value == 2122) {
            this.addColField("rmse-5", "RMSE-5")
          } else if (fnum.value == 2131) {
            this.addColField("acc-1", "ACC-1")
          } else if (fnum.value == 2132) {
            this.addColField("acc-5", "ACC-5")
          }
        }
        console.log(this.data_show_result, "-----------data_show_result.fields--------")
        // this.$nextTick(() => {
          this.redrawChart()
        // })
      },
      deep: true,
    },
    sortedItems: {
      handler(value) {
        console.log(value, "-----------sortedItems--------")
        this.redrawChart()
      },
      deep: true,
    },
    filteredItems: {
      handler(value) {
        console.log(value, "-----------filteredItems--------")
        this.redrawChart()
      },
      deep: true,
    },
  },

  computed: {
    getTruncatedUrl() {
      return (url) => {
        const lastSlashIndex = url.lastIndexOf('/');
        return lastSlashIndex !== -1 ? url.substring(0, lastSlashIndex) : url;
      };
    },
  },
  setup(props, context) {
    const data_show_result = reactive({
      sortedKey: "",
      sortOrders: { "auc-1": 1, "rmse-1": 1, "acc-1": 1, "auc-5": 1, "rmse-5": 1, "acc-5": 1 },
      sortIcons: { "auc-1": 0, "rmse-1": 0, "acc-1": 0, "auc-5": 0, "rmse-5": 0, "acc-5": 0 },
      fixed_fields: [
        [
          { label: "Logs", logurl1: "logurl-1", logurl2: "logurl-5" }
        ], 
        [
          { key: "model", label: "Model" }
        ]
      ],
      fields: [],
      items: [], // 确定显示的模型
    })
    const modelState_change = reactive({
      allSelected: false,
      indeterminate: false,
      selct: [],
    })
    const fold_state = reactive({
      allSelected: false,
      selct: -1,
    })
    const metric_state = reactive({
      allSelected: false,
      indeterminate: false,
      selct: [],
    })
    // 表格操作
    // 增加col名操作
    const addColField = (key, label) => {
      data_show_result.fields.push({ key, label })
    }
    // 增加行数据操作
    const addRowItem = (model) => {
      data_show_result.items.push(props.dataInfo.data_source[model - 1])
    }
    const currentSortedKey = ref('');
    provide('currentSortedKey', currentSortedKey);
    // 排序指标操作
    const sortBy = (key) => {
      data_show_result.sortedKey = key // 排序关键字
      currentSortedKey.value = key.toUpperCase()
      data_show_result.sortOrders[key] = data_show_result.sortOrders[key] * -1 // 关键字排序方向,
      data_show_result.sortIcons[key] = 1
      console.log(data_show_result)
      // redrawChart()
    }
    const sortedItems = computed(() => {
      if (data_show_result.sortedKey) {
        return data_show_result.items.slice().sort((a, b) => {
          if (a[data_show_result.sortedKey] < b[data_show_result.sortedKey]) {
            return data_show_result.sortOrders[data_show_result.sortedKey] * -1
          } else if (a[data_show_result.sortedKey] > b[data_show_result.sortedKey]) {
            return data_show_result.sortOrders[data_show_result.sortedKey] * 1
          }
          return 0
        })
      } else {
        return data_show_result.items
      }
    })

    const searchText = ref('')
  
    const filteredItems = computed(() => {
      const lowerCaseSearchText = searchText.value.toLowerCase();
      return data_show_result.items.filter(item => {
        return item["model"].toLowerCase().includes(lowerCaseSearchText);
      });
    });

    // 监听 searchText 变化，当 searchText 改变时重新过滤数据
    watch(searchText, () => {
      // 在这里可以执行其他逻辑，如果需要的话
      console.log('Search text changed:', searchText.value);
    });
    // 评估指标选择
    const metric_selectPart = () => {
      context.emit("metric_selectPart", metric_state.selct)
    }
    const metric_selectAll = () => {
      context.emit("metric_selectAll", metric_state.allSelected)
    }
    const metric_show = () => {
      context.emit("metric_show")
    }
    const metric_unshow = () => {
      context.emit("metric_unshow")
    }
    // 交叉验证
    const fold_selectPart = () => {
      context.emit("fold_selectPart", fold_state.selct)
    }
    const fold_selectAll = () => {
      context.emit("fold_selectAll", fold_state.allSelected)
    }
    const fold_show = () => {
      context.emit("fold_show")
    }
    const fold_unshow = () => {
      context.emit("fold_unshow")
    }
    // 模型部分
    const model_selectPart = () => {
      context.emit("model_selectPart", modelState_change.selct)
    }
    const model_selectAll = () => {
      context.emit("model_selectAll", modelState_change.allSelected)
    }
    const model_show = () => {
      context.emit("model_show")
    }
    const model_unshow = () => {
      context.emit("model_unshow")
    }

    const chartRef = ref(null)
    let myChart = null
    // 初始化
    const drawChart = () => {
      if (chartRef.value) {
        // 初始化图表
        myChart = echarts.init(chartRef.value)
        // 设置图表横坐标
        // data_show_result.items.map(item => item.model)
        // 设置图表series组
        // let seriesList = []

        // 绘制图表
        let option = {
          tooltip: {
            trigger: "axis",
            axisPointer: { type: "cross" },
          },
          legend: {},
          xAxis: [
            {
              type: "category",
              axisTick: {
                alignWithLabel: true,
                interval: 0,
              },
              axisLabel: {
              interval: 0,
              rotate: 270, // 设置标签旋转角度为270度
            },
              data: data_show_result.items.map((item) => item.model),
            },
          ],
          yAxis: [
            {
              type: "value",
              name: "",
              min: 0,
              max: 1,
              position: "left",
              axisLabel: {
                formatter: "{value}",
              },
            },
          ],
          series: [],
        }
        myChart.setOption(option)
      }
    }
    // 重绘
    const redrawChart = () => {
      let seriesList = [];

      // 排序数据处理 sortedItems (data_show_result.items处理后的)
      if (data_show_result.fields.length > 0) {
        data_show_result.fields.forEach((item) => {
          seriesList.push({
            name: item.label,
            type: "line",
            smooth: false,
            data: sortedItems.value.map((ifem) => ifem[item.key]),
          });
        });
      }

      // 绘制图表
      let option = {
        tooltip: {
          trigger: "axis",
          axisPointer: { type: "cross" },
        },
        legend: {
          bottom: -5, // 设置legend位于图表底部
        },
        xAxis: [
          {
            type: "category",
            axisTick: {
              alignWithLabel: true,
              interval: 0,
            },
            axisLabel: {
              interval: 0,
              rotate: 270, // 设置标签旋转角度为270度
            },
            data: sortedItems.value.map((item) => item.model),
          },
        ],
        yAxis: [
          {
            type: 'value',
            name: "",
            min: 0, // 设置最小值
            max: 1, // 设置最大值
            position: 'left',
            axisLabel: {
              formatter: '{value}'
            }
          },
        ],
        series: seriesList,
      };

      if (seriesList.length != 0) {
        option.yAxis[0].name = seriesList[0]["name"];
        let min_val = Math.min(...seriesList[0].data);
        let max_val = Math.max(...seriesList[0].data);

        option.yAxis[0].min = min_val;
        option.yAxis[0].max = max_val;
        option.series[0]["yAxisIndex"] = 0;

        if (seriesList.length == 2) {
          option.yAxis.push({
            type: 'value',
            name: seriesList[1]["name"],
            min: Math.min(...seriesList[1].data),
            max: Math.max(...seriesList[1].data),
            position: 'right',
            axisLabel: {
              formatter: '{value}'
            }
          })
          option.series[1]['yAxisIndex'] = 1;
        }
      }
      myChart.setOption(option, true);
    };

    onMounted(() => {})

    return {
      data_show_result,
      modelState_change,
      fold_state,
      metric_state,
      sortBy,
      sortedItems,
      searchText,
      filteredItems,
      currentSortedKey,
      addColField,
      addRowItem,
      metric_show,
      metric_unshow,
      metric_selectAll,
      metric_selectPart,
      fold_show,
      fold_unshow,
      fold_selectAll,
      fold_selectPart,
      model_show,
      model_unshow,
      model_selectAll,
      model_selectPart,
      chartRef,
      drawChart,
      redrawChart,
    }
  },
}
</script>

<style scoped>
.om-card-body-content {
  padding: 3px;
  padding-left: 15px;
}

.icon-check-list {
  margin-left: 26px;
  margin-bottom: 5px;
}

.om-col-auto-icon {
  padding-left: 0px;
}

.om-col-auto-form-check {
  padding-right: 8px;
}

h3 {
  font-size: 10px;
  font-weight: bold;
  color: gray;
}

.card-result-home {
  margin-top: 20px;
}
</style>

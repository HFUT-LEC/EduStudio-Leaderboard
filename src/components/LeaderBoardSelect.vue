<template>
  <div class="row select-row">
    <div class="col col-auto left-select">
      <button type="button" class="btn btn-success responsive-text" data-bs-toggle="modal" data-bs-target="#selectModal">
        Task Select
      </button>
      <div class="modal fade" id="selectModal" tabindex="-1" aria-labelledby="selectModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header-part">
              <p class="modal-header-title-name" id="selectModalLabel">
                Please select specific task and operation.
              </p>
            </div>
            <div class="modal-body">
              <div class="card">
                <div class="card-body">
                  <div class="row">
                    <div class="col-2">Task:</div>
                    <div class="col-10">
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="taskRadio" id="taskRadio1"
                          value="CognitiveDiagnosis" v-model="selectedTask" />
                        <label class="form-check-label" for="taskRadio1">
                          Cognitive Diagnosis
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="taskRadio" id="taskRadio2"
                          value="KnowledgeTracing" v-model="selectedTask" />
                        <label class="form-check-label" for="taskRadio2">
                          Knowledge Tracing
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-body">
                  <div class="row">
                    <div class="col-2">Dataset:</div>
                    <div class="col-10" v-if="selectedTask == 'CognitiveDiagnosis'">
                      <div class="form-check form-check-inline" v-for="datset in dataset_show.CognitiveDiagnosis"
                        :key="datset">
                        <input class="form-check-input" type="radio" name="datasetRadio" :id=datset :value=datset
                          v-model="selectedDataset" />
                        <label class="form-check-label" :for=datset>
                          {{ datset }}
                        </label>
                      </div>
                    </div>
                    <div class="col-10" v-if="selectedTask == 'KnowledgeTracing'">
                      <div class="form-check form-check-inline" v-for="datset in dataset_show.KnowledgeTracing"
                        :key="datset">
                        <input class="form-check-input" type="radio" name="datasetRadio" :id=datset :value=datset
                          v-model="selectedDataset" />
                        <label class="form-check-label" :for=datset>
                          {{ datset }}
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-body">
                  <div class="row">
                    <div class="col-2">Application:</div>
                    <div class="col-10" v-if="selectedTask == 'CognitiveDiagnosis'">
                      <div class="form-check form-check-inline" v-for="apply in application_show.CognitiveDiagnosis"
                        :key="apply">
                        <input class="form-check-input" type="radio" name="applyRadio" :id=apply :value=apply
                          v-model="selectedApplication" />
                        <label class="form-check-label" :for=apply>
                          {{ apply }}
                        </label>
                      </div>
                    </div>
                    <div class="col-10" v-if="selectedTask == 'KnowledgeTracing'">
                      <div class="form-check form-check-inline" v-for="apply in application_show.KnowledgeTracing"
                        :key="apply">
                        <input class="form-check-input" type="radio" name="applyRadio" :id=apply :value=apply
                          v-model="selectedApplication" />
                        <label class="form-check-label" :for=apply>
                          {{ apply }}
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                Close
              </button>
              <button @click="refresh" type="button" class="btn btn-primary" data-bs-dismiss="modal">
                Refersh
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-sm right-show-content">
      <div v-if="showContext.is_showed" class="card right-card-show">
        <div class="card-body right-card-body-show">
          <p class="right-card-body-show-content">
            Task: {{ showContext.task }} | Dataset: {{ showContext.dataset }} | Application: {{ showContext.application }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, watch } from "vue";

export default {
  name: "LeaderBoardSelect",
  props: {
    showContext: {
      type: Object,
      required: true,
    },
  },
  setup(props, context) {
    let selectedTask = ref("CognitiveDiagnosis");
    let selectedDataset = ref("");
    let selectedApplication = ref("");
    // 维护: 依据任务需求在此处进行数据集重选择
    const dataset_show = reactive({
      CognitiveDiagnosis: ['FrcSub', 'ASSISTment0910'],
      KnowledgeTracing: ['ASSISTment0910']
    });
    // 维护: 依据任务需求在此处进行应用场景选择, 如General、KnowledgeMissing
    const application_show = reactive({
      CognitiveDiagnosis: ['General',],
      KnowledgeTracing: ['General',]
    });
    // 监听器, 监听selectedTask的变化, 且在回调函数中根据selectedTask的值来更新selectedDataset和selectedApplication的值
    watch(selectedTask, (newValue) => {
      if (newValue == "CognitiveDiagnosis") {
        selectedDataset.value = "";
        selectedApplication.value = "";
      }
      else if (newValue == "KnowledgeTracing") {
        selectedDataset.value = "";
        selectedApplication.value = "";
      }
    });

    const refresh = () => {
      context.emit("refresh", selectedTask.value, selectedDataset.value, selectedApplication.value);
    };

    return {
      selectedTask,
      selectedDataset,
      selectedApplication,
      dataset_show,
      application_show,
      refresh,
    };
  },
};
</script>

<style scoped>
@media (max-width: 1400px) and (min-width: 500px) {
  .right-card-body-show-content {
    font-size: calc(3px + 1vw);

  }
}

.right-card-body-show-content {
  margin: 0px;
  font-weight: bold;
  color: #23272E;
}

.right-card-body-show {
  padding: 0px;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 6px;
}

.right-card-show {
  margin-top: 3px;
  margin-right: 12px;
  display: flex;
}

.modal-header-part {
  padding: 10px;
}

.modal-header-title-name {
  font-size: 15px;
  margin-bottom: 0px;
  color: gray;
}

@media (max-width: 1400px) and (min-width: 500px) {
  .responsive-text {
    white-space: nowrap;
    word-wrap: break-word;
    word-break: break-all;
    font-size: calc(3px + 1vw);
  }
}

.right-show-content {
  padding: 0px;
}

.select-row {
  margin-top: 0px;
}
</style>
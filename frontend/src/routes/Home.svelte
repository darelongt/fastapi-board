<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { page, keyword, is_login} from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')
    let question_list = []

    // function get_question_list() {
    //     fetch("http://127.0.0.1:8000/api/question/list").then((response) => {
    //         response.json().then((json) => {
    //             question_list = json
    //         })
    //     })
    // }
    // function get_question_list() {
    //     fastapi('get', '/api/question/list', {}, (json) => {
    //         question_list = json.question_list
    //     })
    // }
    const P_G_SIZE = 10;
    let size = 10
    let total = 0
    let kw = ''
    $: total_page = Math.ceil(total/size)

    // function get_question_list(_page) {
    //     let params = {
    //         page: _page,
    //         size: size,
    //         keyword: kw,
    //     }
    //     fastapi('get', '/api/question/list', params, (json) => {
    //         question_list = json.question_list
    //         $page = _page
    //         total = json.total
    //     })
    // }

    // $: get_question_list($page)
    function get_question_list() {
        let params = {
            page: $page,
            size: size,
            keyword: $keyword,
        }
        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list
            total = json.total
            kw = $keyword
        })
    }

    $:$page, $keyword, get_question_list()
</script>

<!-- <ul>
    {#each question_list as question}
        <li><a use:link href="/detail/{question.id}">{question.subject}</a></li>
    {/each}
</ul> -->

<div class="container my-3">
    <div class="row my-3">
        <div class="col-6">
            <a use:link href="/question-create" 
                class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value="{kw}">
                <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}}>
                    찾기
                </button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th>번호</th>
            <th style="width:50%">제목</th>
            <th>글쓴이</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, i}
        <tr class="text-center">
            <!-- <td>{i+1}</td> -->
            <td>{ total - ($page * size) - i }</td>
            <td class="text-start">
                <a use:link href="/detail/{question.id}">{question.subject}</a>
                {#if question.answers.length > 0 }
                <span class="text-danger small mx-2">{question.answers.length}</span>
                {/if}
            </td>
            <td>{ question.user ? question.user.username : "" }</td>
            <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
        </tr>
        {/each}
        </tbody>
    </table>
    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {($page < P_G_SIZE) && 'disabled'}">
            <!-- <button class="page-link" on:click="{() => get_question_list(Math.floor($page / P_G_SIZE) * P_G_SIZE - 1)}">&lt;</button> -->
            <button class="page-link" on:click="{() => $page = (Math.floor($page / P_G_SIZE) * P_G_SIZE - 1)}">&lt;</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, pageIndex}
        {#if Math.floor(pageIndex / P_G_SIZE) === Math.floor($page / P_G_SIZE)} 
        <li class="page-item {pageIndex === $page && 'active'}">
            <!-- <button on:click="{() => get_question_list(pageIndex)}" class="page-link pagination-btn">{pageIndex+1}</button> -->
            <button on:click="{() => $page=pageIndex}" class="page-link pagination-btn">{pageIndex+1}</button>
        </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {($page >= total_page - total_page % P_G_SIZE) && 'disabled'}">
            <!-- <button class="page-link" on:click="{() => get_question_list(Math.floor($page / P_G_SIZE) * P_G_SIZE + P_G_SIZE)}">&gt;</button> -->
            <button class="page-link" on:click="{() => $page = (Math.floor($page / P_G_SIZE) * P_G_SIZE + P_G_SIZE)}">&gt;</button>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->
    <!-- <a use:link href="/question-create" class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a> -->
</div>
import axios from '../_snowpack/pkg/axios.v0.22.0.js';
import $ from '../_snowpack/pkg/jquery.v3.6.0.js';


$(document).ready(() => {
    let csrf = $('#csrf_token').val();
    axios.defaults.headers.common["X-CSRFToken"] = csrf;

    let appId = $('#application_id').val();

    axios({
        method: 'get',
        url: `/apply/${ appId }/find_matches`
    }).then(r => {
        let matchesSection = $('#matches');
        r.data.map(m => {
            matchesSection.append(
                `
                <div class="match-box max-w-md">
                  <p class="text-xl">
                    <a href="${ m.url }">${ m.name }</a> at <a href="${ m.org_url }">${ m.org_name }</a> (${ m.location })
                  </p>
                  <div class="detail-container mb-8">
                    <div class="detail-row">
                      <span class="detail-row-header">Provides</span>
                      <span>${ m.matching_analyses.join('<br>') }</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-row-header">Next available</span>
                      <span>${ m.available } to ${ m.until }</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-row-header">Will fund travel</span>
                      <span>${ m.travel_fund ? 'Yes' : 'No' }</span>
                    </div>
                  </div>
                  <input type="submit" data-slot-id="${ m.slot_id }" data-date-from="${ m.available }" data-date-to="${ m.until }" class="match-button p-2" value="Accept">
                </div>
                `
            );
        });
    }).then(() => {
        $('.match-button').click(e => {
            axios.post('/apply/make_match', {
                    app_id: appId,
                    slot_id: e.target.dataset.slotId,
                    date_from: e.target.dataset.dateFrom,
                    date_to: e.target.dataset.dateTo
                }
            ).then((r) => {
                console.log(r);
                window.location.reload(true);
            });
        });
    });
});


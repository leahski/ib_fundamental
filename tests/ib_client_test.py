# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Tests for IBClient"""

import os

import pytest
from ib_async import IB, FundamentalRatios

from ib_fundamental.ib_client import IBClient, Stock, Ticker


class TestIBClient:
    """Test class for IBClient"""

    def test_instantiation(self, ib_client):
        """test IBClient instance"""
        # assert
        assert isinstance(ib_client, IBClient)
        assert isinstance(ib_client.ib, IB)
        assert ib_client.is_connected()

    def test_make_contract(self, ib_client):
        """test IBClient.contract is correct"""
        # assert
        assert isinstance(ib_client.contract, Stock)
        assert ib_client.contract.symbol == ib_client.symbol

    def test_ratios(self, ib_client):
        """Test FundamentalRatios"""
        # act
        _ratio = ib_client.get_ratios()
        # assert
        assert isinstance(_ratio, FundamentalRatios)

    def test_ticker(self, ib_client):
        """Test IBClient.ticker"""
        # arrange
        _ticker = ib_client.get_ticker()
        if _ticker is None:
            while _ticker is None:
                ib_client.ib.sleep(0.0)
        # assert
        assert isinstance(_ticker, Ticker)
        assert _ticker.contract == ib_client.contract

    @pytest.mark.xfail(reason="CalendarReport requires subscription")
    def test_req_fundamental(self, ib_client_req_fund):
        """Test IBClient.ib_req_fund"""
        # arrange
        _report = ib_client_req_fund
        # assert
        assert isinstance(_report, str)

    def test_req_fundamental_error(self, ib_client):
        """Test IBClient.ib_req_fund raises ValueError"""
        # arrange
        _report_type = "CalendarReport"
        with pytest.raises(ValueError) as ex_info:
            _ = ib_client.ib_req_fund(_report_type)
        # assert
        assert ex_info.type is ValueError

    def test_is_connected(self, ib_client):
        """Test IBClient.is_connected"""
        assert ib_client.is_connected()

    def test_disconnect(self, ib_client):
        """Test IBClient.disconnect"""
        # act
        ib_client.disconnect()
        # assert
        assert not ib_client.is_connected()
        # re-connect
        ib_client.ib.connect(
            host=os.getenv("IBFUND_HOST", "localhost"),
            port=int(os.getenv("IBFUND_PORT", "7497")),
            clientId=int(os.getenv("IBFUND_CLI_ID", "120")),
        )
        # assert
        assert ib_client.is_connected()

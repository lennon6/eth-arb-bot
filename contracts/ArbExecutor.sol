// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./interfaces/IUniswapV2Router.sol";
import "./interfaces/ISushiSwapRouter.sol";

interface IERC20 {
    function approve(address spender, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

interface IWETH9 {
    function deposit() external payable;
    function withdraw(uint256 wad) external;
    function approve(address guy, uint256 wad) external returns (bool);
    function transfer(address dst, uint256 wad) external returns (bool);
    function transferFrom(address src, address dst, uint256 wad) external returns (bool);
    function balanceOf(address src) external view returns (uint256);
}

contract ArbitrageExecutor {
    address constant WETH_ADDRESS = 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6;
    address constant UNISWAP_ROUTER_ADDRESS = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address constant SUSHISWAP_ROUTER_ADDRESS = 0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506;
    address constant UNI_TOKEN = 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984;

    IUniswapV2Router private uniswapRouter;
    ISushiSwapRouter private sushiswapRouter;

    constructor() {
        uniswapRouter = IUniswapV2Router(UNISWAP_ROUTER_ADDRESS);
        sushiswapRouter = ISushiSwapRouter(SUSHISWAP_ROUTER_ADDRESS);
    }

    function swap(uint256 _amountIn) external {
        IWETH9(WETH_ADDRESS).transferFrom(msg.sender, address(this), _amountIn);
        IWETH9(WETH_ADDRESS).approve(UNISWAP_ROUTER_ADDRESS, _amountIn);

        address[] memory path = new address[](2);
        path[0] = WETH_ADDRESS;
        path[1] = UNI_TOKEN;

        uint256[] memory amounts = uniswapRouter.swapExactTokensForTokens(
            _amountIn,
            0,
            path,
            address(this),
            block.timestamp
        );
        uint256 amountOut = amounts[1];

        IERC20(UNI_TOKEN).approve(SUSHISWAP_ROUTER_ADDRESS, amountOut);

        path[0] = UNI_TOKEN;
        path[1] = WETH_ADDRESS;

        uint256[] memory amounts_1 = sushiswapRouter.swapExactTokensForTokens(
            amountOut,
            0,
            path,
            msg.sender,
            block.timestamp
        );
        uint256 amountOut_1 = amounts_1[1];

        require(amountOut_1 > _amountIn, "Arbitrage failed!");
    }
}
